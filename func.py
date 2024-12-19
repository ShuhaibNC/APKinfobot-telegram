from asn1crypto import x509
import hashlib
from pyaxmlparser import APK
import asyncio

# Combined MD5 and SHA256 calculation to avoid reading the file twice
def calculate_hashes(file_path):
    md5_hash = hashlib.md5()
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            md5_hash.update(chunk)
            sha256_hash.update(chunk)
    return md5_hash.hexdigest(), sha256_hash.hexdigest()

def get_certificate_info(cert):
    cert_parsed = x509.Certificate.load(cert.dump())
    return (f"Issuer: {cert_parsed.issuer.native}\n"
            f"Subject: {cert_parsed.subject.native}\n"
            f"Serial Number: {cert_parsed.serial_number}\n"
            f"Valid From: {cert_parsed['tbs_certificate']['validity']['not_before'].native}\n"
            f"Valid To: {cert_parsed['tbs_certificate']['validity']['not_after'].native}\n"
            f"Signature Algorithm: {cert_parsed['signature_algorithm']['algorithm'].native}\n"
            f"Public Key Info: {cert_parsed.public_key.native}\n")

# Optional: You can implement this to show progress in long operations
async def progress(current, total):
    percentage = (current / total) * 100
    print(f"Progress: {percentage:.2f}%")

def generate_apk_report(apk_path):
    apk = APK(apk_path)

    # Hash calculations combined into one read operation
    md5_checksum, sha256_checksum = calculate_hashes(apk_path)

    report = [
        f"Package Name: {apk.package}",
        f"Version Name: {apk.version_name}",
        f"Version Code: {apk.version_code}",
        f"Main Activity: {apk.get_main_activity()}",
        f"Minimum SDK Version: {apk.get_min_sdk_version()}",
        f"Target SDK Version: {apk.get_target_sdk_version()}",
        f"Max SDK Version: {apk.get_max_sdk_version()}",
        f"MD5 Checksum: {md5_checksum}",
        f"SHA256 Checksum: {sha256_checksum}"
    ]

    # Streamlined permission/activity/service reporting
    report.extend(format_apk_components("Permissions", apk.get_permissions()))
    report.extend(format_apk_components("Activities", apk.get_activities()))
    report.extend(format_apk_components("Services", apk.get_services()))
    report.extend(format_apk_components("Receivers", apk.get_receivers()))
    report.extend(format_apk_components("Providers", apk.get_providers()))

    # Certificate Info
    report.append("\nCertificate Information:")
    for cert in apk.get_certificates():
        report.append(get_certificate_info(cert))

    return "\n".join(report)

# Helper function to format APK components
def format_apk_components(component_name, components):
    formatted = [f"\n{component_name}:"]
    if not components:
        formatted.append("  - None")
    else:
        for component in components:
            formatted.append(f"  - {component}")
    return formatted
