def select_video(videos, selected_index):
    if 0 <= selected_index < len(videos):
        return videos[selected_index]
    return None
