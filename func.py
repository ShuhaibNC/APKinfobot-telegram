from asn1crypto import x509
import hashlib
from pyaxmlparser import APK

def calculate_md5(file_path):
    md5_hash = hashlib.md5()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            md5_hash.update(chunk)
        f.close()
    return md5_hash.hexdigest()

def calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            sha256_hash.update(chunk)
        f.close()
    return sha256_hash.hexdigest()

def get_certificate_info(cert):
    cert_parsed = x509.Certificate.load(cert.dump())
    return f"Issuer: {cert_parsed.issuer.native}\n" \
           f"Subject: {cert_parsed.subject.native}\n" \
           f"Serial Number: {cert_parsed.serial_number}\n" \
           f"Valid From: {cert_parsed['tbs_certificate']['validity']['not_before'].native}\n" \
           f"Valid To: {cert_parsed['tbs_certificate']['validity']['not_after'].native}\n" \
           f"Signature Algorithm: {cert_parsed['signature_algorithm']['algorithm'].native}\n" \
           f"Public Key Info: {cert_parsed.public_key.native}\n"


async def progress(current, total):
    pass

def generate_apk_report(apk_path):
    apk = APK(apk_path)

    # Basic APK info
    report = []
    report.append(f"Package Name: {apk.package}")
    report.append(f"Version Name: {apk.version_name}")
    report.append(f"Version Code: {apk.version_code}")
    report.append(f"Main Activity: {apk.get_main_activity()}")
    report.append(f"Minimum SDK Version: {apk.get_min_sdk_version()}")
    report.append(f"Target SDK Version: {apk.get_target_sdk_version()}")
    report.append(f"Max SDK Version: {apk.get_max_sdk_version()}")
    report.append(f"MD5 Checksum: {calculate_md5(apk_path)}")
    report.append(f"SHA256 Checksum: {calculate_sha256(apk_path)}")

    # Permissions
    permissions = apk.get_permissions()
    report.append("\nPermissions:")
    for permission in permissions:
        report.append(f"  - {permission}")

    # Activities
    activities = apk.get_activities()
    report.append("\nActivities:")
    for activity in activities:
        report.append(f"  - {activity}")

    # Services
    services = apk.get_services()
    report.append("\nServices:")
    for service in services:
        report.append(f"  - {service}")

    # Receivers
    receivers = apk.get_receivers()
    report.append("\nReceivers:")
    for receiver in receivers:
        report.append(f"  - {receiver}")

    # Providers
    providers = apk.get_providers()
    report.append("\nProviders:")
    for provider in providers:
        report.append(f"  - {provider}")

    # Certificate Info
    certificates = apk.get_certificates()
    report.append("\nCertificate Information:")
    for cert in certificates:
        report.append(get_certificate_info(cert))

    # Save report to file
    full_report = "\n".join(report)
    return full_report
    
    
