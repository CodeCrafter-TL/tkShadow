import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFilter


class Shadow:

    def __init__(self, widgetOrElement: int | tk.Widget, canvas: tk.Canvas,
                 x: tuple[int | float, int | float] | (int | float), y: tuple[int | float, int | float] | (int | float),
                 radius: int | float, color: str) -> None:
        self.widget = widgetOrElement if isinstance(
            widgetOrElement, tk.Widget) else None
        self.element = widgetOrElement if isinstance(
            widgetOrElement, int) else None
        self.canvas = canvas
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.shadow_photo: Image.Image | None = None

        if self.widget:
            self.width = self.widget.winfo_reqwidth()
            self.height = self.widget.winfo_reqheight()
            self.position = self.x[0] + self.width / 2 + \
                self.x[1], self.y[0] + self.height / 2 + self.y[1]
        if self.element:
            self.coords = self.canvas.coords(self.element)
            self.type = self.canvas.type(self.element)
    
    def setGaussianBlur(self, image: Image.Image, radius: int = 5):
        return image.filter(ImageFilter.GaussianBlur(radius))

    def createShadowImage(self):
        if self.widget:
            image = Image.new('RGBA', (self.width + self.radius * 4,
                              self.height + self.radius * 4), (0, 0, 0, 0))
            draw = ImageDraw.Draw(image)
            startPoint = (self.radius * 2, self.radius * 2)
            endPoint = (self.radius * 2 + self.width,
                        self.radius * 2 + self.height)
            draw.rectangle([startPoint, endPoint],
                           fill=self.color, outline=self.color)

            return self.setGaussianBlur(image, self.radius)
        if self.element:
            image = Image.new('RGBA', (int(self.coords[2] - self.coords[0] + self.radius * 4), int(
                self.coords[3] - self.coords[1] + self.radius * 4)), (0, 0, 0, 0))
            draw = ImageDraw.Draw(image)

            match self.type:
                case "oval":
                    draw.ellipse([(10, 10), (self.coords[2] - self.coords[0] + 10,
                                 self.coords[3] - self.coords[1] + 10)], fill=self.color, outline=self.color)
                case "rectangle":
                    draw.rectangle([(10, 10), (self.coords[2] - self.coords[0] + 10,
                                   self.coords[3] - self.coords[1] + 10)], fill=self.color, outline=self.color)
                case el:
                    raise ValueError("您的元素暂不支持添加阴影！")

            return self.setGaussianBlur(image, self.radius)

    def show(self):
        shadow_image = self.createShadowImage()
        if self.widget:
            if shadow_image:
                self.shadow_photo = ImageTk.PhotoImage(shadow_image)
                self.canvas.create_image(
                    self.position[0], self.position[1], image=self.shadow_photo)
                self.shadow_photo = self.shadow_photo
        if self.element:
            if shadow_image:
                self.shadow_photo = ImageTk.PhotoImage(shadow_image)
                imageCanvas = self.canvas.create_image(int(self.coords[2] - self.coords[0]) / 2 + self.x,
                                                       int(self.coords[3] - self.coords[1]) / 2 + self.y, image=self.shadow_photo)
                self.shadow_photo = self.shadow_photo
                self.canvas.lift(self.element, imageCanvas)

    display = shadow = show


# old
class ElementShadow:
    ...


'''
    """
    Create a shadow at Canvas
    id: element id
    canvas: main canvas
    x: center to x
    y: center to y
    blur: blur radius
    color: shadow color
    """

    def __init__(self, id: int, canvas: tk.Canvas, x: int, y: int, blur: int, color: str):
        self.__id = id
        self.canvas = canvas
        self.coords = self.canvas.coords(self.__id)
        print(self.coords)

        self.color = color
        self.x = x - 10
        self.y = y - 10
        self.blur = blur
        self.size = (int(self.coords[2] - self.coords[0]) +
                     20, int(self.coords[3] - self.coords[1]) + 20)
        self.origin_size = (
            int(self.coords[2] - self.coords[0]), int(self.coords[3] - self.coords[1]))

    def create_shadow_image(self):
        """
        Create shadow image using `PIL.Image` and `PIL.ImageDraw`
        """
        item_type = self.canvas.type(self.__id)

        image = Image.new('RGBA', self.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        if item_type == 'oval':
            draw.ellipse(
                [(10, 10), (self.coords[2] - self.coords[0] + 10, self.coords[3] - self.coords[1] + 10)], fill=self.color)
        if item_type == 'rectangle':
            draw.rectangle([(10, 10), (self.coords[2] - self.coords[0] +
                           10, self.coords[3] - self.coords[1] + 10)], fill=self.color)

        shadow_image = setGaussianBlur(image, self.blur)
        return shadow_image

    def show(self):
        """
        Create shadow image at Canvas
        """
        shadow_image = self.create_shadow_image()
        shadow_photo = ImageTk.PhotoImage(shadow_image)

        self.shadow_x = int(self.x + self.origin_size[0] - 10)
        self.shadow_y = int(self.y + self.origin_size[1] - 10)
        print(self.coords)
        print(self.shadow_x, self.shadow_y)
        print(self.origin_size[0], self.origin_size[1])

        self.shadow = self.canvas.create_image(
            self.shadow_x, self.shadow_y, image=shadow_photo)
        self.canvas.lift(self.__id, self.shadow)
        self.shadow_photo = shadow_photo'''


# Example usage:
if __name__ == "__main__":
    root = tk.Tk()
    canvas = tk.Canvas(root, width=400, height=400, bg="#ffffff")
    canvas.pack()

    oval = canvas.create_oval(5, 5, 55, 55, fill='red', outline='red')
    # re = canvas.create_rectangle(5, 5, 60, 80, fill='red', outline='red')

    # test = tk.Label(canvas, text="Hello World")
    # test.place(x=100, y=100)
    shadow = Shadow(oval, canvas, 5, 5, 5, "#000000")
    shadow.display()

    root.mainloop()
