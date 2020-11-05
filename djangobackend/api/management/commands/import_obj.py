import os
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from api.models import Asset, Vulnerability, VulnStatus, User
from djangobackend.keyconfig import User as test_user


def read_csv(filepath='./api/management/commands/'):
        result = []
        csv_files = []
        for entry in os.scandir(filepath):
            if(entry.path.endswith('.csv')):
                csv_files.append(entry.path)
        
        for file in csv_files:
            with open(file, 'r') as f:
                content = f.read()
                # Split content based on lines, except the first
                content = content.split('\n')[1:]
                
                result += content
            
        # Quicksort lines based on ASSET - HOSTNAME to optimize object importing
        result.sort()

        return result

def normalize_data(arr):
    """
    Fix possible input file format errors (extra commas, empty lines, etc)
    """
    for index, item in enumerate(arr):
        if item == ['']:
            arr.pop(index)
        elif len(item) > 6:
            for i in range(len(item) - 6):
                item[2] += item[3]
                item.pop(3)
    
    return arr

def create_test_user():
    """
    creates a dummy user for testing purposes
    """
    if not User.objects.filter(username=test_user.USERNAME):
        User.objects.create_user(username=test_user.USERNAME, password1=test_user.PASSWORD, password2=test_user.PASSWORD)


class Command(BaseCommand):
    help = ""

    def handle(self, *args, **options):
        
        print("Import command is running")

        # Array containing lines from file
        data = read_csv()
        # Splits each array on the comma
        data = list(map(lambda x: x.split(','), data))
        # data order: hostname, ipv4, vuln, severity, cvss, pub_date        
        data = normalize_data(data)

        asset = None
        for index, line in enumerate(data):
            if not asset:
                asset = Asset.objects.get_or_create(
                    hostname=line[0],
                    ip_address=line[1]
                )[0]
            else:
                # Checks if asset is the same as last iteration to re-use it
                if asset.hostname != data[index-1][0].lower():
                    asset = Asset.objects.get_or_create(
                        hostname=line[0],
                        ip_address=line[1]
                    )[0]
            
            # Normalizes the date
            date = datetime.strptime(line[5], "%Y-%m-%d") if line[5] != '' else None
            # Normalizes the cvss
            cvss = line[4] if line[4]!='' else None
            # Get or create the vulnerability
            vuln = Vulnerability.objects.get_or_create(
                title=line[2],
                defaults={
                    'severity': line[3],
                    'cvss': cvss,
                    'pub_date': date
                }
            )[0]

            sts, created = VulnStatus.objects.get_or_create(asset=asset, vulnerability=vuln)
            
            if created:
                print("Created VulnStatus asset:{} vuln:{} ".format(sts.asset.hostname, sts.vulnerability.title))
            else:
                print("FAILED - Relation already exists asset: {} vuln: {} ".format(asset.hostname, vuln.title))

        create_test_user()

