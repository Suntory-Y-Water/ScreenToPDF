import flet as ft


def main(page: ft.Page):

    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_visible = True

    top_left_x = ft.TextField(
        hint_text="左上 X座標", expand=True, bgcolor=ft.colors.WHITE24)
    top_left_y = ft.TextField(
        hint_text="左上 Y座標", expand=True, bgcolor=ft.colors.WHITE24)
    bottom_right_x = ft.TextField(
        hint_text="右下 X座標", expand=True, bgcolor=ft.colors.WHITE24)
    bottom_right_y = ft.TextField(
        hint_text="右下 Y座標", expand=True, bgcolor=ft.colors.WHITE24)

    locate_edits = ft.Column(
        width=100,
        controls=[
            ft.Row(
                controls=[
                    top_left_x,
                    top_left_y,
                    bottom_right_x,
                    bottom_right_y
                ],
            ),
        ],
    )

    left_view = ft.Column(
        [
            ft.Row(
                [
                    ft.Container(
                        content=locate_edits,
                        # bgcolor=ft.colors.WHITE38,
                        margin=15,
                        padding=50,
                        width=582,
                        height=375,
                        border_radius=10,
                    ),
                    ft.Container(
                        content=ft.Container(
                            theme=ft.Theme(color_scheme=ft.ColorScheme(
                                primary=ft.colors.PINK_100)),
                            padding=10,
                            margin=100,
                            theme_mode=ft.ThemeMode.LIGHT,
                            content=ft.OutlinedButton(
                                text="スクリーンショット撮影",
                            )
                        ),
                        margin=10,
                        padding=30,
                        width=582,
                        height=375,
                        border_radius=10,
                    )
                ]
            )
        ]
    )

    def pick_files_result(e: ft.FilePickerResultEvent):
        selected_files.value = (
            ", ".join(map(lambda f: f.name, e.files)
                      ) if e.files else "Cancelled!"
        )
        selected_files.update()

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    selected_files = ft.Text(
                        size=20,
                        color=ft.colors.WHITE,
                        weight=ft.FontWeight.NORMAL,
                    )

    page.overlay.append(pick_files_dialog)

    right_view = ft.Column(
        [
            ft.Row(
                [
                    ft.Container(
                        content=ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Container(
                                        content=ft.OutlinedButton(
                                            "Pick files",
                                            icon=ft.icons.UPLOAD_FILE,
                                            on_click=lambda _: pick_files_dialog.pick_files(
                                                allow_multiple=True
                                            ),
                                        ),
                                        theme=ft.Theme(color_scheme=ft.ColorScheme(primary=ft.colors.PINK_100)),
                                        width=325,
                                        height=100,                                   
                                        border_radius=10,
                                    ),                        
                                    selected_files
                                ],
                            ),
                            alignment=ft.alignment.center,
                            margin=ft.margin.only(top=100),
                        ),
                        margin=10,
                        padding=30,
                        width=582,
                        height=375,
                        border_radius=10,
                    ),
                    ft.Container(
                        content=ft.Container(
                            theme=ft.Theme(color_scheme=ft.ColorScheme(
                                primary=ft.colors.PINK_100)),
                            padding=10,
                            margin=100,
                            theme_mode=ft.ThemeMode.LIGHT,
                            content=ft.OutlinedButton(
                                text="PDF作成",
                            )
                        ),
                        margin=10,
                        padding=30,
                        width=582,
                        height=375,
                        border_radius=10,
                    )
                ]
            )
        ]
    )

    t = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        label_color=ft.colors.PINK_100,
        overlay_color="hovered",
        width=1220,
        height=650,
        indicator_padding=10,
        tabs=[
            ft.Tab(
                text="スクリーンショット実施",
                content=left_view,
            ),
            ft.Tab(
                text="PDF作成",
                content=right_view
            ),
        ],
    )
    page.add(t)
    


if __name__ == '__main__':
    ft.app(target=main)
