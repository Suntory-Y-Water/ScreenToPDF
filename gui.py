import flet as ft

def main(page: ft.Page):

    t = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        label_color="#C7243A",
        overlay_color="hovered",
        tabs=[
            ft.Tab(
                text="スクリーンショット",
                content=ft.Container(
                    content=ft.Text("スクリーンショット作成画面のレイアウト"), alignment=ft.alignment.center
                ),
            ),
            ft.Tab(
                text="PDF作成",
                content=ft.Container(
                    content=ft.Text("PDF作成画面のレイアウト"), alignment=ft.alignment.center
                ),
            ),
        ],
        expand=1,
    )

    page.add(t)

ft.app(target=main)