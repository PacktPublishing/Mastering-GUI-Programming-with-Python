# Mastering GUI Programming with Python

<packt link><img src="" alt="Mastering GUI Programming with Python" height="256px" align="right"></a>

This is the code repository for [Mastering GUI Programming with Python](packt link), published by Packt.

**Develop impressive cross-platform GUI applications with PyQt**

## What is this book about?
PyQt5 has long been the most powerful and comprehensive GUI framework available for Python, yet there is a lack of cohesive resources available to teach Python programmers how to use it. This book aims to remedy the problem by providing comprehensive coverage of GUI development with PyQt5. 

You will get started with an introduction to PyQt5, before going on to develop stunning GUIs with modern features. You will then learn how to build forms using QWidgets and learn about important aspects of GUI development such as layouts, size policies, and event-driven programming. Moving ahead, you’ll discover PyQt5’s most powerful features through chapters on audio-visual programming with QtMultimedia, database-driven software with QtSQL, and web browsing with QtWebEngine. Next, in-depth coverage of multithreading and asynchronous programming will help you run tasks asynchronously and build high-concurrency processes with ease. In later chapters, you’ll gain insights into QOpenGLWidget, along with mastering techniques for creating 2D graphics with QPainter. You’ll also explore PyQt on a Raspberry Pi and interface it with remote systems using QtNetwork. Finally, you will learn how to distribute your applications using setuptools and PyInstaller.

By the end of this book, you will have the skills you need to develop robust GUI applications using PyQt.

This book covers the following exciting features:
- Get to grips with the inner workings of PyQt5
- Learn how elements in a GUI application communicate with signals and slots
- Learn techniques for styling an application
- Explore database-driven applications with the QtSQL module
- Create 2D graphics with QPainter
- Delve into 3D graphics with QOpenGLWidget
- Build network and web-aware applications with QtNetwork and QtWebEngine


If you feel this book is for you, get your [copy](https://www.amazon.com/dp/1-789-61290-X) today!

<a href="https://www.packtpub.com/?utm_source=github&utm_medium=banner&utm_campaign=GitHubBanner"><img src="https://raw.githubusercontent.com/PacktPublishing/GitHub/master/GitHub.png" 
alt="https://www.packtpub.com/" border="5" /></a>

## Instructions and Navigations
All of the code is organized into folders. For example, Chapter03.

The code will look like the following:
```
 # inside __init__()
        self.goodbutton = qtw.QPushButton("Good")
        self.layout().addWidget(self.goodbutton)
        self.goodbutton.clicked.connect(self.no_args)
        # ...

    def no_args(self):
        print('I need no arguments')
```

**Following is what you need for this book:**
This book is for programmers who want to create attractive, functional, and powerful GUIs using the Python language. You’ll also find this book useful if you are a student, professional, or anyone who wants to start exploring GUIs or take your skills to the next level. Although prior knowledge of the Python language is assumed, experience with PyQt, Qt, or GUI programming is not required.

With the following software and hardware list you can run all code files present in the book (Chapter 1-17).
### Software and Hardware List
| Chapter | Software required | OS required |
| -------- | ------------------------------------ | ----------------------------------- |
| 1 - 17 | Python 3.7 or greater, PyQt 5.12 | Windows, Mac OS X, and Linux (Any) |
| 17 | PyInstaller 3.4, SetupTools 41.0.1 | Windows, Mac OS X, and Linux (Any) |
| 1-4 | QtDesigner/QtCreator 4.8.0 or higher | Windows, Mac OS X, and Linux (Any) |
| 9 | SQLite 3 | Windows, Mac OS X, and Linux (Any) |
| 12, 14 | psutil 5.6.2 | Windows, Mac OS X, and Linux (Any) |
| 15 | Raspberry Pi 3B+, Raspbian 10 | Windows, Mac OS X, and Linux (Any) |


We also provide a PDF file that has color images of the screenshots/diagrams used in this book. [Click here to download it](http://www.packtpub.com/sites/default/files/downloads/9781789612905_ColorImages.pdf).

## Code in Action

Click on the following link to see the Code in Action:[Click here to view the videos](http://bit.ly/2M3QVrl)

### Related products
* Qt5 Python GUI Programming Cookbook [[Packt]](https://www.packtpub.com/application-development/qt5-python-gui-programming-cookbook?utm_source=github&utm_medium=repository&utm_campaign=) [[Amazon]](https://www.amazon.com/dp/B079S4Q9T2)

* Mastering OpenCV 4 with Python [[Packt]](https://www.packtpub.com/application-development/mastering-opencv-4-python?utm_source=github&utm_medium=repository&utm_campaign=) [[Amazon]](https://www.amazon.com/dp/B07Q85SJLK)


## Get to Know the Author
**Alan D Moore**
is a data analyst and software developer who has been solving problems with Python since 2006. He's developed both open source and private code using frameworks like Django, Flask, Qt, and, Tkinter, and contributes to various open source Python and Javascript projects. Alan is the author of Python GUI Programming with Tkinter.



## Other books by the authors
[Python GUI programming with Tkinter](https://www.packtpub.com/application-development/python-gui-programming-tkinter?utm_source=github&utm_medium=repository&utm_campaign=)


### Suggestions and Feedback
[Click here](https://docs.google.com/forms/d/e/1FAIpQLSdy7dATC6QmEL81FIUuymZ0Wy9vH1jHkvpY57OiMeKGqib_Ow/viewform) if you have any feedback or suggestions.


