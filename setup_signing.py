
import base64
import hashlib
import json
from pathlib import Path
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec

root = Path(__file__).resolve().parent
updates = root / "updates"
resource = updates / "resources" / "filters.txt"
manifest_path = updates / "manifest.json"
signature_path = updates / "manifest.sig"
private_path = root / "private_signing_key.pem"
public_path = root / "public_key.txt"

if not resource.exists():
    raise SystemExit(f"Missing resource file: {resource}")

# Keep the private signing key on this PC.
if private_path.exists():
    private_key = serialization.load_pem_private_key(
        private_path.read_bytes(), password=None
    )
    print("Using existing private signing key.")
else:
    private_key = ec.generate_private_key(ec.SECP256R1())
    private_path.write_bytes(
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
    )
    print("Created a new private signing key.")

public_der = private_key.public_key().public_bytes(
    encoding=serialization.Encoding.DER,
    format=serialization.PublicFormat.SubjectPublicKeyInfo,
)
public_b64 = base64.b64encode(public_der).decode("ascii")
public_path.write_text(public_b64 + "\n", encoding="ascii")

resource_bytes = resource.read_bytes()
resource_url = (
    "https://raw.githubusercontent.com/ddread-gif/"
    "OpenMedia-Filter-Updates/main/updates/resources/filters.txt"
)

manifest = {
    "versionCode": 2,
    "minAppVersionCode": 1,
    "maxAppVersionCode": 0,
    "formatVersion": 1,
    "sizeBytes": len(resource_bytes),
    "sha256": hashlib.sha256(resource_bytes).hexdigest(),
    "resourceUrl": resource_url,
}

manifest_bytes = (
    json.dumps(manifest, indent=2) + "\n"
).encode("utf-8")
manifest_path.write_bytes(manifest_bytes)

signature = private_key.sign(
    manifest_bytes,
    ec.ECDSA(hashes.SHA256()),
)
signature_path.write_text(
    base64.b64encode(signature).decode("ascii") + "\n",
    encoding="ascii",
)

gitignore = root / ".gitignore"
existing = gitignore.read_text(encoding="utf-8") if gitignore.exists() else ""
if "private_signing_key.pem" not in existing:
    with gitignore.open("a", encoding="utf-8") as f:
        f.write("\n# Never upload the private signing key\nprivate_signing_key.pem\n")

print("\nSUCCESS: manifest created and signed.")
print("Public key saved to:", public_path)
print("Manifest:", manifest_path)
print("Signature:", signature_path)
print("\nCOPY THIS PUBLIC KEY INTO UpdateConfig.kt:\n")
print(public_b64)
print("\nIMPORTANT: Never upload private_signing_key.pem.")
