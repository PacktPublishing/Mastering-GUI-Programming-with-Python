#version 120

attribute highp vec4 vertex;
uniform highp mat4 matrix;
attribute lowp vec4 color_attr;
varying lowp vec4 color;

void main(void)
{
  gl_Position = matrix * vertex;
  color = color_attr;
}
