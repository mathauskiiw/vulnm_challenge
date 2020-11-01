import os
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from api.models import Asset, Vulnerability, VulnStatus

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

class Command(BaseCommand):
    help = ""

    def handle(self, *args, **options):
        
        print("Import command is running")
        # Array containing lines from file
        data = read_csv()
        # Splits each array on the comma
        data = list(map(lambda x: x.split(','), data))
        # data order: hostname, ipv4, vuln, severity, cvss, pub_date
        
        data = data[1:]
        print(data)

        asset = None
        for index, line in enumerate(data):
            print(line)
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
                print("FAILED - Relation already exists asset:{} vuln:{} ".format(asset.hostname, vuln.title))

         

    