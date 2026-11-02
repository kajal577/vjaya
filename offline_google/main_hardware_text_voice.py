        memory_dc.SetBkMode(win32con.TRANSPARENT)
        memory_dc.FillSolidRect(
            (0, 0, OLED_WIDTH, OLED_HEIGHT),
            win32api.RGB(0, 0, 0)
        )

        return (
            screen_handle, screen_dc, memory_dc,
            bitmap, font, old_bitmap, old_font
        )

    except Exception:
        win32gui.ReleaseDC(0, screen_handle)
        raise


def close_text_dc(resources):
    """Safely release Windows drawing resources."""
    if not resources:
        return

    (
        screen_handle,
        screen_dc,
        memory_dc,
        bitmap,
        font,
        old_bitmap,
        old_font
    ) = resources

    try:
        # Restore the original font and bitmap before deleting objects.
        try:
            memory_dc.SelectObject(old_font)
        except Exception:
            pass

        try:
            memory_dc.SelectObject(old_bitmap)
        except Exception:
            pass

        # Delete the compatible memory device context.
        try:
            memory_dc.DeleteDC()
        except Exception:
            pass

        # Delete GDI objects through win32gui, not wrapper methods.
        try:
            win32gui.DeleteObject(bitmap.GetHandle())
        except Exception:
            pass

        try:
            win32gui.DeleteObject(font.GetSafeHandle())
        except Exception:
            pass

    finally:
        # A DC obtained with GetDC must be released with ReleaseDC.
        win32gui.ReleaseDC(0, screen_handle)




def clean_text(text):
    text = str(text)
    text = text.replace("|", " ")
    text = text.replace("\r", " ").replace("\n", " ")
    return " ".join(text.split())


def measure_text_width(dc, text):
    size = dc.GetTextExtent(text)
    return size[0]


def wrap_text_pixels(text):
    """Wrap words using Windows font measurements."""
    text = clean_text(text)

    if not text:
        return []

    resources = create_text_dc()
    dc = resources[2]

    try:
        words = text.split()
        lines = []
        current = ""

        for word in words:
            candidate = word if not current else current + " " + word

            if measure_text_width(dc, candidate) <= OLED_MAX_TEXT_WIDTH:
                current = candidate
            else:
                if current:
                    lines.append(current)

                # Never split a Hindi word or its vowel marks.
                current = word

        if current:
            lines.append(current)

        return lines

    finally:
        close_text_dc(resources)


def render_oled_bitmap(text_lines):
    """Render text to a 128x64 monochrome bitmap."""
    resources = create_text_dc()
    dc = resources[2]

    try:
        all_lines = []

        for item in text_lines:
            all_lines.extend(wrap_text_pixels(item))

        all_lines = all_lines[:OLED_LINES_PER_PAGE]

        for index, line in enumerate(all_lines):
            y = index * OLED_LINE_HEIGHT

            rect = (
                0, y,
                OLED_WIDTH, y + OLED_LINE_HEIGHT
            )

            dc.DrawText(
                line,
                rect,
                win32con.DT_LEFT
                | win32con.DT_TOP
                | win32con.DT_SINGLELINE
                | win32con.DT_NOPREFIX
            )

        # Convert white pixels into the MSB-first bitmap format
        # expected by Adafruit_GFX drawBitmap().
        bitmap_data = bytearray(
            OLED_WIDTH * OLED_HEIGHT // 8
        )

        for y in range(OLED_HEIGHT):
            for x in range(OLED_WIDTH):
                pixel = win32gui.GetPixel(
                    dc.GetSafeHdc(), x, y
                )

                if pixel != win32api.RGB(0, 0, 0):
                    byte_index = (y * OLED_WIDTH + x) // 8
                    bit_index = 7 - (x % 8)