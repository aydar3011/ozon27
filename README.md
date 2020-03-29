Программ для генерации отчета интернет-магазина Озон по выборке "Продукты питания"
Программа выполнена на языке python2.7 
Необходимые модули:
  1. selenium
  2. bs4
  3. requests
  4. fake_useragent
  5. wget
  6. pillow
  7. rtfw
В файле ozon.py происходит извлечение данных со страницы озон при помощи selenium и bs4.
В файле writertf.py при помощи модуля rtfw генерируется rtf файл

Для корректной работы rtfw с русским языком необходимо:
1) В модуле pyRTF/PropertySets.py находим класс Font
    class Font :
      def __init__( self, name, family, character_set = 0, pitch = None, panose = None, alternate = None ) :
и заменяем в этой строке character_set = 0 на character_set = 204

2) В модуле pyRTF/Elements.py находим строки идущие подряд (всего 28 штук):
StandardFonts.append( Font( 'Arial', 'swiss' , 0, 2, '020b0604020202020204' ) )
...
...
StandardFonts.append( Font( 'Verdana', 'swiss' , 0, 2, '020b0604030504040204' ) )
И в них всех (кроме единственной StandardFonts.append( Font( ‘Symbol’, ‘roman’ , 2, 2, ‘05050102010706020507’ ) )) заменяем третий аргумент - 0(ноль) идущий после ‘swiss’ меняем на 204.

3) В модуле pyRTF/Constants.py находим класс Languages и атрибут DEFAULT=EnglishAustralian меняем на DEFAULT=Russian

4) В модуле pyRTF/Renderer.py находим класс Renderer, у него ищем метод _WriteDocument( self ) и в нем в строчке
self._write( "{\\rtf1\\ansi\\ansicpg1252\\deff0%s\n" % settings )
меняем ansicpg1252 на ansicpg1251.
  
