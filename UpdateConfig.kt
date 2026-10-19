package com.openmedia.app.updater

object UpdateConfig {
    private const val BASE =
        "https://raw.githubusercontent.com/ddread-gif/OpenMedia-Filter-Updates/main/updates"

    const val MANIFEST_URL = "$BASE/manifest.json"
    const val SIGNATURE_URL = "$BASE/manifest.sig"
    const val PUBLIC_KEY_X509_BASE64 = "MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEuyN6nALt86jyMt00HqDnAPOsesX/JIlZEU8fA4UB4Nh2O2PBjjT5LQ/xfNwh8kS/tZNqsDlC7KnMndnDGwqWiw=="
    const val MAX_RESOURCE_BYTES = 10L * 1024 * 1024
    const val MAX_MANIFEST_BYTES = 32 * 1024L
    const val SUPPORTED_FORMAT_VERSION = 1
    const val CONNECT_TIMEOUT_MS = 10000
    const val READ_TIMEOUT_MS = 20000
    const val WORK_NAME = "filter-resource-update"
}
