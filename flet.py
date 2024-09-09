import flet as ft

def main(page: ft.Page):
    page.title = "Список акций"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    stocks = {
    "AAPL": 100.0,
    "GOOG": 2000.0,
    "MSFT": 150.0,
    "TSLA": 300.0
    }

    def on_stock_click(e):
        e.control.selected = not e.control.selected
        page.update()

    def on_stock_press(e):
        e.control.selected = not e.control.selected
        page.update()
        
    class StockCard(ft.Card):
        def __init__(self, stock, price):
            super().__init__()

            self.stock = stock
            self.price = price
            self.content = ft.Container(
                              
                content=ft.ListTile(
                    hover_color=ft.colors.AMBER_200,
                    selected_color=ft.colors.GREEN_200,
                    leading=ft.Icon(ft.icons.STORE),
                    icon_color=ft.colors.AMBER_800,

                    title=ft.Row(
                        controls=[ft.Text(self.stock), ft.Text(self.price)],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                    autofocus=True,
                    selected=False, 
                    subtitle=ft.Text(self.price),

                    selected_tile_color=ft.colors.GREEN_500,
                    shape=ft.RoundedRectangleBorder(radius=10),

                    on_click=on_stock_click,
                    on_long_press=on_stock_press                   
                ),
                padding=ft.padding.all(0)
            )
    
    for stock, price in stocks.items():
        page.add(
            ft.Column(
                [
                    StockCard(stock, price),
                ],
                alignment="center",
            )
        )

ft.app(target=main)
