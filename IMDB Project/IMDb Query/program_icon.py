def get_icon_base64():
    img_b64 = b'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'
    return img_b64