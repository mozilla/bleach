import html5lib
from nose.tools import eq_

import bleach

def method():
    eq_(,bleach.clean('<XML ID="xss"><I><B><IMG SRC="javas<!-- -->cript:alert('XSS')"></B></I></XML>'))

def test_image_js_src():
    eq_(u'&lt;img src="javascript:alert(\'XXS\');"&gt;', bleach.clean('<IMG SRC="javascript:alert(\'XSS\');">'))

def test_image_js_src_no_quotes():
    eq_(u'&lt;img src="javascript:alert(\'XSS\')"&gt;', bleach.clean("<IMG SRC=javascript:alert('XSS')>"))

def test_image_js_src_no_quotes_casing():
    eq_(u'&lt;img src="javascript:alert(\'XSS\')"&gt;', bleach.clean("<IMG SRC=JaVaScRiPt:alert('XSS')>"))
	

def test_image_js_src_dbl_quotes():
    eq_(u'&lt;img src="javascript:alert(\"XSS\")"&gt;', bleach.clean("<IMG SRC=javascript:alert(\"XSS\")>"))
	
def test_image_js_src_dbl_quotes():
    eq_(u'&lt;img src="`javascript:alert("RSnake says, \'xss\'")`=""&gt;', bleach.clean('<IMG SRC=`javascript:alert("RSnake says, \'XSS\'")`>'))

# regex pull needs to be formatted and rename
	
def test_image_malformed():
    eq_(,bleach.clean('<IMG """><SCRIPT>alert("XSS")</SCRIPT>">'))

def test_image_from_char_code():
    eq_(,bleach.clean('<IMG SRC=javascript:alert(String.fromCharCode(88,83,83))>'))

def test_image_src_hashtag():
    eq_(,bleach.clean('<IMG SRC=# onmouseover="alert('xxs')">'))

def test_image_empty_src():
    eq_(,bleach.clean('<IMG SRC= onmouseover="alert('xxs')">'))

def test_image_no_src():
    eq_(,bleach.clean('<IMG onmouseover="alert(\'xxs\')">'))

def test_image_decimal_html_character():
    eq_(,bleach.clean('<IMG SRC=&#106;&#97;&#118;&#97;&#115;&#99;&#114;&#105;&#112;&#116;&#58;&#97;&#108;&#101;&#114;&#116;&#40;&#39;&#88;&#83;&#83;&#39;&#41;>'))

def test_image_decimal_html_character_no_semi():
    eq_(,bleach.clean('<IMG SRC=&#0000106&#0000097&#0000118&#0000097&#0000115&#0000099&#0000114&#0000105&#0000112&#0000116&#0000058&#0000097&#0000108&#0000101&#0000114&#0000116&#0000040&#0000039&#0000088&#0000083&#0000083&#0000039&#0000041>'))

def test_image_hexadecimal_html_character_no_semi():
    eq_(,bleach.clean('<IMG SRC=&#x6A&#x61&#x76&#x61&#x73&#x63&#x72&#x69&#x70&#x74&#x3A&#x61&#x6C&#x65&#x72&#x74&#x28&#x27&#x58&#x53&#x53&#x27&#x29>'))

def test_image_embedded_tab():
    eq_(,bleach.clean('<IMG SRC="jav	ascript:alert('XSS');">'))

def test_image_embedded_encoded_tab():
    eq_(,bleach.clean('<IMG SRC="jav&#x09;ascript:alert('XSS');">'))

def test_image_embedded_newline():
    eq_(,bleach.clean('<IMG SRC="jav&#x0A;ascript:alert('XSS');">'))

def test_image_embedded_carriage():
    eq_(,bleach.clean('<IMG SRC="jav&#x0D;ascript:alert('XSS');">'))

def test_image_embedded_metachar_and_space():
    eq_(,bleach.clean('<IMG SRC=" &#14;  javascript:alert('XSS');">'))

def method():
    eq_(,bleach.clean('<IMG SRC="javascript:alert('XSS')"'))

def method():
    eq_(,bleach.clean('<IMG DYNSRC="javascript:alert('XSS')">'))
	
def method():
    eq_(,bleach.clean('<IMG LOWSRC="javascript:alert('XSS')">'))

def method():
    eq_(,bleach.clean('<IMG SRC='vbscript:msgbox("XSS")'>'))

def method():
    eq_(,bleach.clean('<IMG SRC="livescript:[code]">'))

def method():
    eq_(,bleach.clean('<IMG SRC="javascript:alert('XSS');">'))

def method():
    eq_(,bleach.clean('<IMG SRC=javascript:alert('XSS')>'))

def method():
    eq_(,bleach.clean('<IMG SRC=JaVaScRiPt:alert('XSS')>'))

def method():
    eq_(,bleach.clean('<IMG SRC=javascript:alert("XSS")>'))

def method():
    eq_(,bleach.clean('<IMG SRC=`javascript:alert("RSnake says, 'XSS'")`>'))

def method():
    eq_(,bleach.clean('<IMG """><SCRIPT>alert("XSS")</SCRIPT>">'))

def method():
    eq_(,bleach.clean('<IMG SRC=javascript:alert(String.fromCharCode(88,83,83))>'))

def method():
    eq_(,bleach.clean('<IMG SRC=# onmouseover="alert('xxs')">'))

def method():
    eq_(,bleach.clean('<IMG SRC= onmouseover="alert('xxs')">'))

def method():
    eq_(,bleach.clean('<IMG onmouseover="alert('xxs')">'))

def method():
    eq_(,bleach.clean('<IMG SRC=&#106;&#97;&#118;&#97;&#115;&#99;&#114;&#105;&#112;&#116;&#58;&#97;&#108;&#101;&#114;&#116;&#40;'))
	
def method():
    eq_(,bleach.clean('<IMG SRC=&#x6A&#x61&#x76&#x61&#x73&#x63&#x72&#x69&#x70&#x74&#x3A&#x61&#x6C&#x65&#x72&#x74&#x28&#x27&#x58&#x53&#x53&#x27&#x29>'))

def method():
    eq_(,bleach.clean('<IMG SRC="jav	ascript:alert('XSS');">'))

def method():
    eq_(,bleach.clean('<IMG SRC="jav&#x09;ascript:alert('XSS');">'))

def method():
    eq_(,bleach.clean('<IMG SRC="jav&#x0A;ascript:alert('XSS');">'))

def method():
    eq_(,bleach.clean('<IMG SRC="jav&#x0D;ascript:alert('XSS');">'))
	
def method():
    eq_(,bleach.clean('<IMG SRC=" &#14;  javascript:alert('XSS');">'))	
	
def method():
    eq_(,bleach.clean('<IMG STYLE="xss:expr/*XSS*/ession(alert('XSS'))">'))	
	
def method():
    eq_(,bleach.clean('<IMG SRC="http://www.thesiteyouareon.com/somecommand.php?somevariables=maliciouscode">'))	

def method():
    eq_(,bleach.clean('<IMG SRC=&#0000106&#0000097&#0000118&#0000097&#0000115&#0000099&#0000114&#0000105&#0000112&#0000116&#0000058&#0000097&'))

def method():
    eq_(,bleach.clean('<IMG SRC="javascript:alert('XSS')"'))

def method():
    eq_(,bleach.clean('<IMG DYNSRC="javascript:alert('XSS')">'))

def method():
    eq_(,bleach.clean('<IMG LOWSRC="javascript:alert('XSS')">'))

def method():
    eq_(,bleach.clean('<IMG SRC='vbscript:msgbox("XSS")'>'))

def method():
    eq_(,bleach.clean('<IMG SRC="livescript:[code]">'))

def method():
    eq_(,bleach.clean('<IMG STYLE="xss:expr/*XSS*/ession(alert('XSS'))">'))

def method():
    eq_(,bleach.clean('<XML ID="xss"><I><B><IMG SRC="javas<!-- -->cript:alert('XSS')"></B></I></XML>'))

























	
#end of image test

