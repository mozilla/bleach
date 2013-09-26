import html5lib
from nose.tools import eq_

import bleach

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
	
def method():
    eq(,bleach.clean('';alert(String.fromCharCode(88,83,83))//';alert(String.fromCharCode(88,83,83))//";'))

def method():
    eq(,bleach.clean('alert(String.fromCharCode(88,83,83))//";alert(String.fromCharCode(88,83,83))//--'))

def method():
    eq(,bleach.clean('></SCRIPT>">'><SCRIPT>alert(String.fromCharCode(88,83,83))</SCRIPT>'))

def method():
    eq(,bleach.clean(''';!--"<XSS>=&{()}'))

def method():
    eq(,bleach.clean('<SCRIPT SRC=http://ha.ckers.org/xss.js></SCRIPT>'))

def method():
    eq(,bleach.clean('<IMG SRC="javascript:alert('XSS');">'))

def method():
    eq(,bleach.clean('<IMG SRC=javascript:alert('XSS')>'))

def method():
    eq(,bleach.clean('<IMG SRC=JaVaScRiPt:alert('XSS')>'))

def method():
    eq(,bleach.clean('<IMG SRC=javascript:alert("XSS")>'))

def method():
    eq(,bleach.clean('<IMG SRC=`javascript:alert("RSnake says, 'XSS'")`>'))

def method():
    eq(,bleach.clean('<IMG """><SCRIPT>alert("XSS")</SCRIPT>">'))

def method():
    eq(,bleach.clean('<IMG SRC=javascript:alert(String.fromCharCode(88,83,83))>'))

def method():
    eq(,bleach.clean('<IMG SRC=# onmouseover="alert('xxs')">'))

def method():
    eq(,bleach.clean('<IMG SRC= onmouseover="alert('xxs')">'))

def method():
    eq(,bleach.clean('<IMG onmouseover="alert('xxs')">'))

def method():
    eq(,bleach.clean('<IMG SRC=&#106;&#97;&#118;&#97;&#115;&#99;&#114;&#105;&#112;&#116;&#58;&#97;&#108;&#101;&#114;&#116;&#40;'))

def method():
    eq(,bleach.clean('&#39;&#88;&#83;&#83;&#39;&#41;>'))

def method():
    eq(,bleach.clean('<IMG SRC=&#0000106&#0000097&#0000118&#0000097&#0000115&#0000099&#0000114&#0000105&#0000112&#0000116&#0000058&#0000097&'))

def method():
    eq(,bleach.clean('#0000108&#0000101&#0000114&#0000116&#0000040&#0000039&#0000088&#0000083&#0000083&#0000039&#0000041>'))

def method():
    eq(,bleach.clean('<IMG SRC=&#x6A&#x61&#x76&#x61&#x73&#x63&#x72&#x69&#x70&#x74&#x3A&#x61&#x6C&#x65&#x72&#x74&#x28&#x27&#x58&#x53&#x53&#x27&#x29>'))

def method():
    eq(,bleach.clean('<IMG SRC="jav	ascript:alert('XSS');">'))

def method():
    eq(,bleach.clean('<IMG SRC="jav&#x09;ascript:alert('XSS');">'))

def method():
    eq(,bleach.clean('<IMG SRC="jav&#x0A;ascript:alert('XSS');">'))

def method():
    eq(,bleach.clean('<IMG SRC="jav&#x0D;ascript:alert('XSS');">'))

def method():
    eq(,bleach.clean('perl -e 'print "<IMG SRC=java\0script:alert(\"XSS\")>";' > out'))

def method():
    eq(,bleach.clean('<IMG SRC=" &#14;  javascript:alert('XSS');">'))

def method():
    eq(,bleach.clean('<SCRIPT/XSS SRC="http://ha.ckers.org/xss.js"></SCRIPT>'))

def method():
    eq(,bleach.clean('<BODY onload!#$%&()*~+-_.,:;?@[/|\]^`=alert("XSS")>'))

def method():
    eq(,bleach.clean('<SCRIPT/SRC="http://ha.ckers.org/xss.js"></SCRIPT>'))

def method():
    eq(,bleach.clean('<<SCRIPT>alert("XSS");//<</SCRIPT>'))

def method():
    eq(,bleach.clean('<SCRIPT SRC=http://ha.ckers.org/xss.js?< B >'))

def method():
    eq(,bleach.clean('<SCRIPT SRC=//ha.ckers.org/.j>'))

def method():
    eq(,bleach.clean('<IMG SRC="javascript:alert('XSS')"'))

def method():
    eq(,bleach.clean('<iframe src=http://ha.ckers.org/scriptlet.html <'))

def method():
    eq(,bleach.clean('\";alert('XSS');//'))

def method():
    eq(,bleach.clean('</TITLE><SCRIPT>alert("XSS");</SCRIPT>'))

def method():
    eq(,bleach.clean('<INPUT TYPE="IMAGE" SRC="javascript:alert('XSS');">'))

def method():
    eq(,bleach.clean('<BODY BACKGROUND="javascript:alert('XSS')">'))

def method():
    eq(,bleach.clean('<IMG DYNSRC="javascript:alert('XSS')">'))

def method():
    eq(,bleach.clean('<IMG LOWSRC="javascript:alert('XSS')">'))

def method():
    eq(,bleach.clean('<STYLE>li {list-style-image: url("javascript:alert('XSS')");}</STYLE><UL><LI>XSS</br>'))

def method():
    eq(,bleach.clean('<IMG SRC='vbscript:msgbox("XSS")'>'))

def method():
    eq(,bleach.clean('<IMG SRC="livescript:[code]">'))

def method():
    eq(,bleach.clean('<BODY ONLOAD=alert('XSS')>'))

def method():
    eq(,bleach.clean('<BGSOUND SRC="javascript:alert('XSS');">'))

def method():
    eq(,bleach.clean('<BR SIZE="&{alert('XSS')}">'))

def method():
    eq(,bleach.clean('<LINK REL="stylesheet" HREF="javascript:alert('XSS');">'))

def method():
    eq(,bleach.clean('<LINK REL="stylesheet" HREF="http://ha.ckers.org/xss.css">'))

def method():
    eq(,bleach.clean('<STYLE>@import'http://ha.ckers.org/xss.css';</STYLE>'))

def method():
    eq(,bleach.clean('<META HTTP-EQUIV="Link" Content="<http://ha.ckers.org/xss.css>; REL=stylesheet">'))

def method():
    eq(,bleach.clean('<STYLE>BODY{-moz-binding:url("http://ha.ckers.org/xssmoz.xml#xss")}</STYLE>'))

def method():
    eq(,bleach.clean('<STYLE>@im\port'\ja\vasc\ript:alert("XSS")';</STYLE>'))

def method():
    eq(,bleach.clean('<IMG STYLE="xss:expr/*XSS*/ession(alert('XSS'))">'))

def method():
    eq(,bleach.clean('exp/*<A STYLE='no\xss:noxss("*//*");'))

def method():
    eq(,bleach.clean('xss:ex/*XSS*//*/*/pression(alert("XSS"))'>'))

def method():
    eq(,bleach.clean('<STYLE TYPE="text/javascript">alert('XSS');</STYLE>'))

def method():
    eq(,bleach.clean('<STYLE>.XSS{background-image:url("javascript:alert('XSS')");}</STYLE><A CLASS=XSS></A>'))

def method():
    eq(,bleach.clean('<STYLE type="text/css">BODY{background:url("javascript:alert('XSS')")}</STYLE>'))

def method():
    eq(,bleach.clean('<XSS STYLE="xss:expression(alert('XSS'))">'))

def method():
    eq(,bleach.clean('<XSS STYLE="behavior: url(xss.htc);">'))

def method():
    eq(,bleach.clean('¼script¾alert(¢XSS¢)¼/script¾'))

def method():
    eq(,bleach.clean('<META HTTP-EQUIV="refresh" CONTENT="0;url=javascript:alert('XSS');">'))

def method():
    eq(,bleach.clean('<META HTTP-EQUIV="refresh" CONTENT="0;url=data:text/html base64,PHNjcmlwdD5hbGVydCgnWFNTJyk8L3NjcmlwdD4K">'))

def method():
    eq(,bleach.clean('<META HTTP-EQUIV="refresh" CONTENT="0; URL=http://;URL=javascript:alert('XSS');">'))

def method():
    eq(,bleach.clean('<IFRAME SRC="javascript:alert('XSS');"></IFRAME>'))

def method():
    eq(,bleach.clean('<IFRAME SRC=# onmouseover="alert(document.cookie)"></IFRAME>'))

def method():
    eq(,bleach.clean('<FRAMESET><FRAME SRC="javascript:alert('XSS');"></FRAMESET>'))

def method():
    eq(,bleach.clean('<TABLE BACKGROUND="javascript:alert('XSS')">'))

def method():
    eq(,bleach.clean('<TABLE><TD BACKGROUND="javascript:alert('XSS')">'))

def method():
    eq(,bleach.clean('<DIV STYLE="background-image: url(javascript:alert('XSS'))">'))

def method():
    eq(,bleach.clean('<DIV STYLE="background-image:\0075\0072\006C\0028'\006a\0061\0076\0061\0073\0063\0072\0069\0070\0074\003a\0061\006c\0065\0072\0074\0028.1027\0058.1053\0053\0027\0029'\0029">'))

def method():
    eq(,bleach.clean('<DIV STYLE="background-image: url(&#1;javascript:alert('XSS'))">'))

def method():
    eq(,bleach.clean('<DIV STYLE="width: expression(alert('XSS'));">'))

def method():
    eq(,bleach.clean('<!--[if gte IE 4]>'))

def method():
    eq(,bleach.clean(' <SCRIPT>alert('XSS');</SCRIPT>'))

def method():
    eq(,bleach.clean(' <![endif]-->'))

def method():
    eq(,bleach.clean('<BASE HREF="javascript:alert('XSS');//">'))

def method():
    eq(,bleach.clean(' <OBJECT TYPE="text/x-scriptlet" DATA="http://ha.ckers.org/scriptlet.html"></OBJECT>'))

def method():
    eq(,bleach.clean('EMBED SRC="http://ha.ckers.Using an EMBED tag you can embed a Flash movie that contains XSS. Click here for a demo. If you add the attributes allowScriptAccess="never" and allownetworking="internal" it can mitigate this risk (thank you to Jonathan Vanasco for the info).:'))

def method():
    eq(,bleach.clean('org/xss.swf" AllowScriptAccess="always"></EMBED>'))

def method():
    eq(,bleach.clean('<EMBED SRC="data:image/svg+xml;base64,PHN2ZyB4bWxuczpzdmc9Imh0dH A6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcv MjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hs aW5rIiB2ZXJzaW9uPSIxLjAiIHg9IjAiIHk9IjAiIHdpZHRoPSIxOTQiIGhlaWdodD0iMjAw IiBpZD0ieHNzIj48c2NyaXB0IHR5cGU9InRleHQvZWNtYXNjcmlwdCI+YWxlcnQoIlh TUyIpOzwvc2NyaXB0Pjwvc3ZnPg==" type="image/svg+xml" AllowScriptAccess="always"></EMBED>'))

def method():
    eq(,bleach.clean('a="get";'))

def method():
    eq(,bleach.clean('b="URL(\"";'))

def method():
    eq(,bleach.clean('c="javascript:";'))

def method():
    eq(,bleach.clean('d="alert('XSS');\")";'))

def method():
    eq(,bleach.clean('eval(a+b+c+d);'))

def method():
    eq(,bleach.clean('<XML ID="xss"><I><B><IMG SRC="javas<!-- -->cript:alert('XSS')"></B></I></XML>'))

def method():
    eq(,bleach.clean('<SPAN DATASRC="#xss" DATAFLD="B" DATAFORMATAS="HTML"></SPAN>'))

def method():
    eq(,bleach.clean('<XML SRC="xsstest.xml" ID=I></XML>'))

def method():
    eq(,bleach.clean('<SPAN DATASRC=#I DATAFLD=C DATAFORMATAS=HTML></SPAN>'))

def method():
    eq(,bleach.clean('<HTML><BODY>'))

def method():
    eq(,bleach.clean('<?xml:namespace prefix="t" ns="urn:schemas-microsoft-com:time">'))

def method():
    eq(,bleach.clean('<?import namespace="t" implementation="#default#time2">'))

def method():
    eq(,bleach.clean('<t:set attributeName="innerHTML" to="XSS<SCRIPT DEFER>alert("XSS")</SCRIPT>">'))

def method():
    eq(,bleach.clean('</BODY></HTML>'))

def method():
    eq(,bleach.clean('<SCRIPT SRC="http://ha.ckers.org/xss.jpg"></SCRIPT>'))

def method():
    eq(,bleach.clean('<!--#exec cmd="/bin/echo '<SCR'"--><!--#exec cmd="/bin/echo 'IPT SRC=http://ha.ckers.org/xss.js></SCRIPT>'"-->'))

def method():
    eq(,bleach.clean('<? echo('<SCR)';'))

def method():
    eq(,bleach.clean('echo('IPT>alert("XSS")</SCRIPT>'); ?>'))

def method():
    eq(,bleach.clean('<IMG SRC="http://www.thesiteyouareon.com/somecommand.php?somevariables=maliciouscode">'))

def method():
    eq(,bleach.clean('Redirect 302 /a.jpg http://victimsite.com/admin.asp&deleteuser'))

def method():
    eq(,bleach.clean('<META HTTP-EQUIV="Set-Cookie" Content="USERID=<SCRIPT>alert('XSS')</SCRIPT>">'))

def method():
    eq(,bleach.clean(' <HEAD><META HTTP-EQUIV="CONTENT-TYPE" CONTENT="text/html; charset=UTF-7"> </HEAD>+ADw-SCRIPT+AD4-alert('XSS');+ADw-/SCRIPT+AD4-'))

def method():
    eq(,bleach.clean('<SCRIPT a=">" SRC="http://ha.ckers.org/xss.js"></SCRIPT>'))

def method():
    eq(,bleach.clean('<SCRIPT =">" SRC="http://ha.ckers.org/xss.js"></SCRIPT>'))

def method():
    eq(,bleach.clean('<SCRIPT a=">" '' SRC="http://ha.ckers.org/xss.js"></SCRIPT>'))

def method():
    eq(,bleach.clean('<SCRIPT "a='>'" SRC="http://ha.ckers.org/xss.js"></SCRIPT>'))

def method():
    eq(,bleach.clean('<SCRIPT a=`>` SRC="http://ha.ckers.org/xss.js"></SCRIPT>'))

def method():
    eq(,bleach.clean('<SCRIPT a=">'>" SRC="http://ha.ckers.org/xss.js"></SCRIPT>'))

def method():
    eq(,bleach.clean('<SCRIPT>document.write("<SCRI");</SCRIPT>PT SRC="http://ha.ckers.org/xss.js"></SCRIPT>'))

def method():
    eq(,bleach.clean('<A HREF="http://66.102.7.147/">XSS</A>'))

def method():
    eq(,bleach.clean('<A HREF="http://%77%77%77%2E%67%6F%6F%67%6C%65%2E%63%6F%6D">XSS</A>'))

def method():
    eq(,bleach.clean('<A HREF="http://1113982867/">XSS</A>'))

def method():
    eq(,bleach.clean('<A HREF="http://0x42.0x0000066.0x7.0x93/">XSS</A>'))

def method():
    eq(,bleach.clean('<A HREF="http://0102.0146.0007.00000223/">XSS</A>'))

def method():
    eq(,bleach.clean('<A HREF="h'))

def method():
    eq(,bleach.clean('tt	p://6	6.000146.0x7.147/">XSS</A>'))

def method():
    eq(,bleach.clean('<A HREF="//www.google.com/">XSS</A>'))

def method():
    eq(,bleach.clean('<A HREF="//google">XSS</A>'))

def method():
    eq(,bleach.clean('<A HREF="http://ha.ckers.org@google">XSS</A>'))

def method():
    eq(,bleach.clean('<A HREF="http://google:ha.ckers.org">XSS</A>'))

def method():
    eq(,bleach.clean('<A HREF="http://google.com/">XSS</A>'))

def method():
    eq(,bleach.clean('<A HREF="http://www.google.com./">XSS</A>'))

def method():
    eq(,bleach.clean('<A HREF="javascript:document.location='http://www.google.com/'">XSS</A>'))

def method():
    eq(,bleach.clean('<A HREF="http://www.gohttp://www.google.com/ogle.com/">XSS</A>'))

def method():
    eq(,bleach.clean('<'))

def method():
    eq(,bleach.clean('%3C'))

def method():
    eq(,bleach.clean('&lt'))

def method():
    eq(,bleach.clean('&lt;'))

def method():
    eq(,bleach.clean('&LT'))

def method():
    eq(,bleach.clean('&LT;'))

def method():
    eq(,bleach.clean('&#60'))

def method():
    eq(,bleach.clean('&#060'))

def method():
    eq(,bleach.clean('&#0060'))

def method():
    eq(,bleach.clean('&#00060'))

def method():
    eq(,bleach.clean('&#000060'))

def method():
    eq(,bleach.clean('&#0000060'))

def method():
    eq(,bleach.clean('<'))

def method():
    eq(,bleach.clean('&#060;'))

def method():
    eq(,bleach.clean('&#0060;'))

def method():
    eq(,bleach.clean('&#00060;'))

def method():
    eq(,bleach.clean('&#000060;'))

def method():
    eq(,bleach.clean('&#0000060;'))

def method():
    eq(,bleach.clean('&#x3c'))

def method():
    eq(,bleach.clean('&#x03c'))

def method():
    eq(,bleach.clean('&#x003c'))

def method():
    eq(,bleach.clean('&#x0003c'))

def method():
    eq(,bleach.clean('&#x00003c'))

def method():
    eq(,bleach.clean('&#x000003c'))

def method():
    eq(,bleach.clean('&#x3c;'))

def method():
    eq(,bleach.clean('&#x03c;'))

def method():
    eq(,bleach.clean('&#x003c;'))

def method():
    eq(,bleach.clean('&#x0003c;'))

def method():
    eq(,bleach.clean('&#x00003c;'))

def method():
    eq(,bleach.clean('&#x000003c;'))

def method():
    eq(,bleach.clean('&#X3c'))

def method():
    eq(,bleach.clean('&#X03c'))

def method():
    eq(,bleach.clean('&#X003c'))

def method():
    eq(,bleach.clean('&#X0003c'))

def method():
    eq(,bleach.clean('&#X00003c'))

def method():
    eq(,bleach.clean('&#X000003c'))

def method():
    eq(,bleach.clean('&#X3c;'))

def method():
    eq(,bleach.clean('&#X03c;'))

def method():
    eq(,bleach.clean('&#X003c;'))

def method():
    eq(,bleach.clean('&#X0003c;'))

def method():
    eq(,bleach.clean('&#X00003c;'))

def method():
    eq(,bleach.clean('&#X000003c;'))

def method():
    eq(,bleach.clean('&#x3C'))

def method():
    eq(,bleach.clean('&#x03C'))

def method():
    eq(,bleach.clean('&#x003C'))

def method():
    eq(,bleach.clean('&#x0003C'))

def method():
    eq(,bleach.clean('&#x00003C'))

def method():
    eq(,bleach.clean('&#x000003C'))

def method():
    eq(,bleach.clean('&#x3C;'))

def method():
    eq(,bleach.clean('&#x03C;'))

def method():
    eq(,bleach.clean('&#x003C;'))

def method():
    eq(,bleach.clean('&#x0003C;'))

def method():
    eq(,bleach.clean('&#x00003C;'))

def method():
    eq(,bleach.clean('&#x000003C;'))

def method():
    eq(,bleach.clean('&#X3C'))

def method():
    eq(,bleach.clean('&#X03C'))

def method():
    eq(,bleach.clean('&#X003C'))

def method():
    eq(,bleach.clean('&#X0003C'))

def method():
    eq(,bleach.clean('&#X00003C'))

def method():
    eq(,bleach.clean('&#X000003C'))

def method():
    eq(,bleach.clean('&#X3C;'))

def method():
    eq(,bleach.clean('&#X03C;'))

def method():
    eq(,bleach.clean('&#X003C;'))

def method():
    eq(,bleach.clean('&#X0003C;'))

def method():
    eq(,bleach.clean('&#X00003C;'))

def method():
    eq(,bleach.clean('&#X000003C;'))

def method():
    eq(,bleach.clean('\x3c'))

def method():
    eq(,bleach.clean('\x3C'))

def method():
    eq(,bleach.clean('\u003c'))

def method():
    eq(,bleach.clean('\u003C'))

def method():
    eq(,bleach.clean('jQuery.fn.jQuery.init[106]'))

def method():
    eq(,bleach.clean('tags.each(function(){console.log($(this).html())})'))

def method():
    eq(,bleach.clean('';alert(String.fromCharCode(88,83,83))//';alert(String.fromCharCode(88,83,83))//";'))

def method():
    eq(,bleach.clean('alert(String.fromCharCode(88,83,83))//";alert(String.fromCharCode(88,83,83))//--'))

def method():
    eq(,bleach.clean('></SCRIPT>">'><SCRIPT>alert(String.fromCharCode(88,83,83))</SCRIPT>'))

def method():
    eq(,bleach.clean(''';!--"<XSS>=&{()}'))

def method():
    eq(,bleach.clean('<SCRIPT SRC=http://ha.ckers.org/xss.js></SCRIPT>'))

def method():
    eq(,bleach.clean('<IMG SRC="javascript:alert('XSS');">'))

def method():
    eq(,bleach.clean('<IMG SRC=javascript:alert('XSS')>'))

def method():
    eq(,bleach.clean('<IMG SRC=JaVaScRiPt:alert('XSS')>'))

def method():
    eq(,bleach.clean('<IMG SRC=javascript:alert("XSS")>'))

def method():
    eq(,bleach.clean('<IMG SRC=`javascript:alert("RSnake says, 'XSS'")`>'))

def method():
    eq(,bleach.clean('<IMG """><SCRIPT>alert("XSS")</SCRIPT>">'))

def method():
    eq(,bleach.clean('<IMG SRC=javascript:alert(String.fromCharCode(88,83,83))>'))

def method():
    eq(,bleach.clean('<IMG SRC=# onmouseover="alert('xxs')">'))

def method():
    eq(,bleach.clean('<IMG SRC= onmouseover="alert('xxs')">'))

def method():
    eq(,bleach.clean('<IMG onmouseover="alert('xxs')">'))

def method():
    eq(,bleach.clean('<IMG SRC=&#106;&#97;&#118;&#97;&#115;&#99;&#114;&#105;&#112;&#116;&#58;&#97;&#108;&#101;&#114;&#116;&#40;'))

def method():
    eq(,bleach.clean('&#39;&#88;&#83;&#83;&#39;&#41;>'))

def method():
    eq(,bleach.clean('<IMG SRC=&#0000106&#0000097&#0000118&#0000097&#0000115&#0000099&#0000114&#0000105&#0000112&#0000116&#0000058&#0000097&'))

def method():
    eq(,bleach.clean('#0000108&#0000101&#0000114&#0000116&#0000040&#0000039&#0000088&#0000083&#0000083&#0000039&#0000041>'))

def method():
    eq(,bleach.clean('<IMG SRC=&#x6A&#x61&#x76&#x61&#x73&#x63&#x72&#x69&#x70&#x74&#x3A&#x61&#x6C&#x65&#x72&#x74&#x28&#x27&#x58&#x53&#x53&#x27&#x29>'))

def method():
    eq(,bleach.clean('<IMG SRC="jav	ascript:alert('XSS');">'))

def method():
    eq(,bleach.clean('<IMG SRC="jav&#x09;ascript:alert('XSS');">'))

def method():
    eq(,bleach.clean('<IMG SRC="jav&#x0A;ascript:alert('XSS');">'))

def method():
    eq(,bleach.clean('<IMG SRC="jav&#x0D;ascript:alert('XSS');">'))

def method():
    eq(,bleach.clean('perl -e 'print "<IMG SRC=java\0script:alert(\"XSS\")>";' > out'))

def method():
    eq(,bleach.clean('<IMG SRC=" &#14;  javascript:alert('XSS');">'))

def method():
    eq(,bleach.clean('<SCRIPT/XSS SRC="http://ha.ckers.org/xss.js"></SCRIPT>'))

def method():
    eq(,bleach.clean('<BODY onload!#$%&()*~+-_.,:;?@[/|\]^`=alert("XSS")>'))

def method():
    eq(,bleach.clean('<SCRIPT/SRC="http://ha.ckers.org/xss.js"></SCRIPT>'))

def method():
    eq(,bleach.clean('<<SCRIPT>alert("XSS");//<</SCRIPT>'))

def method():
    eq(,bleach.clean('<SCRIPT SRC=http://ha.ckers.org/xss.js?< B >'))

def method():
    eq(,bleach.clean('<SCRIPT SRC=//ha.ckers.org/.j>'))

def method():
    eq(,bleach.clean('<IMG SRC="javascript:alert('XSS')"'))

def method():
    eq(,bleach.clean('<iframe src=http://ha.ckers.org/scriptlet.html <'))

def method():
    eq(,bleach.clean('\";alert('XSS');//'))

def method():
    eq(,bleach.clean('</TITLE><SCRIPT>alert("XSS");</SCRIPT>'))

def method():
    eq(,bleach.clean('<INPUT TYPE="IMAGE" SRC="javascript:alert('XSS');">'))

def method():
    eq(,bleach.clean('<BODY BACKGROUND="javascript:alert('XSS')">'))

def method():
    eq(,bleach.clean('<IMG DYNSRC="javascript:alert('XSS')">'))

def method():
    eq(,bleach.clean('<IMG LOWSRC="javascript:alert('XSS')">'))

def method():
    eq(,bleach.clean('<STYLE>li {list-style-image: url("javascript:alert('XSS')");}</STYLE><UL><LI>XSS</br>'))

def method():
    eq(,bleach.clean('<IMG SRC='vbscript:msgbox("XSS")'>'))

def method():
    eq(,bleach.clean('<IMG SRC="livescript:[code]">'))

def method():
    eq(,bleach.clean('<BODY ONLOAD=alert('XSS')>'))

def method():
    eq(,bleach.clean('<BGSOUND SRC="javascript:alert('XSS');">'))

def method():
    eq(,bleach.clean('<BR SIZE="&{alert('XSS')}">'))

def method():
    eq(,bleach.clean('<LINK REL="stylesheet" HREF="javascript:alert('XSS');">'))

def method():
    eq(,bleach.clean('<LINK REL="stylesheet" HREF="http://ha.ckers.org/xss.css">'))

def method():
    eq(,bleach.clean('<STYLE>@import'http://ha.ckers.org/xss.css';</STYLE>'))

def method():
    eq(,bleach.clean('<META HTTP-EQUIV="Link" Content="<http://ha.ckers.org/xss.css>; REL=stylesheet">'))

def method():
    eq(,bleach.clean('<STYLE>BODY{-moz-binding:url("http://ha.ckers.org/xssmoz.xml#xss")}</STYLE>'))

def method():
    eq(,bleach.clean('<STYLE>@im\port'\ja\vasc\ript:alert("XSS")';</STYLE>'))

def method():
    eq(,bleach.clean('<IMG STYLE="xss:expr/*XSS*/ession(alert('XSS'))">'))

def method():
    eq(,bleach.clean('exp/*<A STYLE='no\xss:noxss("*//*");'))

def method():
    eq(,bleach.clean('xss:ex/*XSS*//*/*/pression(alert("XSS"))'>'))

def method():
    eq(,bleach.clean('<STYLE TYPE="text/javascript">alert('XSS');</STYLE>'))

def method():
    eq(,bleach.clean('<STYLE>.XSS{background-image:url("javascript:alert('XSS')");}</STYLE><A CLASS=XSS></A>'))

def method():
    eq(,bleach.clean('<STYLE type="text/css">BODY{background:url("javascript:alert('XSS')")}</STYLE>'))

def method():
    eq(,bleach.clean('<XSS STYLE="xss:expression(alert('XSS'))">'))

def method():
    eq(,bleach.clean('<XSS STYLE="behavior: url(xss.htc);">'))

def method():
    eq(,bleach.clean('¼script¾alert(¢XSS¢)¼/script¾'))

def method():
    eq(,bleach.clean('<META HTTP-EQUIV="refresh" CONTENT="0;url=javascript:alert('XSS');">'))

def method():
    eq(,bleach.clean('<META HTTP-EQUIV="refresh" CONTENT="0;url=data:text/html base64,PHNjcmlwdD5hbGVydCgnWFNTJyk8L3NjcmlwdD4K">'))

def method():
    eq(,bleach.clean('<META HTTP-EQUIV="refresh" CONTENT="0; URL=http://;URL=javascript:alert('XSS');">'))

def method():
    eq(,bleach.clean('<IFRAME SRC="javascript:alert('XSS');"></IFRAME>'))

def method():
    eq(,bleach.clean('<IFRAME SRC=# onmouseover="alert(document.cookie)"></IFRAME>'))

def method():
    eq(,bleach.clean('<FRAMESET><FRAME SRC="javascript:alert('XSS');"></FRAMESET>'))

def method():
    eq(,bleach.clean('<TABLE BACKGROUND="javascript:alert('XSS')">'))

def method():
    eq(,bleach.clean('<TABLE><TD BACKGROUND="javascript:alert('XSS')">'))

def method():
    eq(,bleach.clean('<DIV STYLE="background-image: url(javascript:alert('XSS'))">'))

def method():
    eq(,bleach.clean('<DIV STYLE="background-image:\0075\0072\006C\0028'\006a\0061\0076\0061\0073\0063\0072\0069\0070\0074\003a\0061\006c\0065\0072\0074\0028.1027\0058.1053\0053\0027\0029'\0029">'))

def method():
    eq(,bleach.clean('<DIV STYLE="background-image: url(&#1;javascript:alert('XSS'))">'))

def method():
    eq(,bleach.clean('<DIV STYLE="width: expression(alert('XSS'));">'))

def method():
    eq(,bleach.clean('<!--[if gte IE 4]>'))

def method():
    eq(,bleach.clean(' <SCRIPT>alert('XSS');</SCRIPT>'))

def method():
    eq(,bleach.clean(' <![endif]-->'))

def method():
    eq(,bleach.clean('<BASE HREF="javascript:alert('XSS');//">'))

def method():
    eq(,bleach.clean(' <OBJECT TYPE="text/x-scriptlet" DATA="http://ha.ckers.org/scriptlet.html"></OBJECT>'))

def method():
    eq(,bleach.clean('EMBED SRC="http://ha.ckers.Using an EMBED tag you can embed a Flash movie that contains XSS. Click here for a demo. If you add the attributes allowScriptAccess="never" and allownetworking="internal" it can mitigate this risk (thank you to Jonathan Vanasco for the info).:'))

def method():
    eq(,bleach.clean('org/xss.swf" AllowScriptAccess="always"></EMBED>'))

def method():
    eq(,bleach.clean('<EMBED SRC="data:image/svg+xml;base64,PHN2ZyB4bWxuczpzdmc9Imh0dH A6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcv MjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hs aW5rIiB2ZXJzaW9uPSIxLjAiIHg9IjAiIHk9IjAiIHdpZHRoPSIxOTQiIGhlaWdodD0iMjAw IiBpZD0ieHNzIj48c2NyaXB0IHR5cGU9InRleHQvZWNtYXNjcmlwdCI+YWxlcnQoIlh TUyIpOzwvc2NyaXB0Pjwvc3ZnPg==" type="image/svg+xml" AllowScriptAccess="always"></EMBED>'))

def method():
    eq(,bleach.clean('a="get";'))

def method():
    eq(,bleach.clean('b="URL(\"";'))

def method():
    eq(,bleach.clean('c="javascript:";'))

def method():
    eq(,bleach.clean('d="alert('XSS');\")";'))

def method():
    eq(,bleach.clean('eval(a+b+c+d);'))

def method():
    eq(,bleach.clean('<XML ID="xss"><I><B><IMG SRC="javas<!-- -->cript:alert('XSS')"></B></I></XML>'))

def method():
    eq(,bleach.clean('<SPAN DATASRC="#xss" DATAFLD="B" DATAFORMATAS="HTML"></SPAN>'))

def method():
    eq(,bleach.clean('<XML SRC="xsstest.xml" ID=I></XML>'))

def method():
    eq(,bleach.clean('<SPAN DATASRC=#I DATAFLD=C DATAFORMATAS=HTML></SPAN>'))

def method():
    eq(,bleach.clean('<HTML><BODY>'))

def method():
    eq(,bleach.clean('<?xml:namespace prefix="t" ns="urn:schemas-microsoft-com:time">'))

def method():
    eq(,bleach.clean('<?import namespace="t" implementation="#default#time2">'))

def method():
    eq(,bleach.clean('<t:set attributeName="innerHTML" to="XSS<SCRIPT DEFER>alert("XSS")</SCRIPT>">'))

def method():
    eq(,bleach.clean('</BODY></HTML>'))

def method():
    eq(,bleach.clean('<SCRIPT SRC="http://ha.ckers.org/xss.jpg"></SCRIPT>'))

def method():
    eq(,bleach.clean('<!--#exec cmd="/bin/echo '<SCR'"--><!--#exec cmd="/bin/echo 'IPT SRC=http://ha.ckers.org/xss.js></SCRIPT>'"-->'))

def method():
    eq(,bleach.clean('<? echo('<SCR)';'))

def method():
    eq(,bleach.clean('echo('IPT>alert("XSS")</SCRIPT>'); ?>'))

def method():
    eq(,bleach.clean('<IMG SRC="http://www.thesiteyouareon.com/somecommand.php?somevariables=maliciouscode">'))

def method():
    eq(,bleach.clean('Redirect 302 /a.jpg http://victimsite.com/admin.asp&deleteuser'))

def method():
    eq(,bleach.clean('<META HTTP-EQUIV="Set-Cookie" Content="USERID=<SCRIPT>alert('XSS')</SCRIPT>">'))

def method():
    eq(,bleach.clean(' <HEAD><META HTTP-EQUIV="CONTENT-TYPE" CONTENT="text/html; charset=UTF-7"> </HEAD>+ADw-SCRIPT+AD4-alert('XSS');+ADw-/SCRIPT+AD4-'))

def method():
    eq(,bleach.clean('<SCRIPT a=">" SRC="http://ha.ckers.org/xss.js"></SCRIPT>'))

def method():
    eq(,bleach.clean('<SCRIPT =">" SRC="http://ha.ckers.org/xss.js"></SCRIPT>'))

def method():
    eq(,bleach.clean('<SCRIPT a=">" '' SRC="http://ha.ckers.org/xss.js"></SCRIPT>'))

def method():
    eq(,bleach.clean('<SCRIPT "a='>'" SRC="http://ha.ckers.org/xss.js"></SCRIPT>'))

def method():
    eq(,bleach.clean('<SCRIPT a=`>` SRC="http://ha.ckers.org/xss.js"></SCRIPT>'))

def method():
    eq(,bleach.clean('<SCRIPT a=">'>" SRC="http://ha.ckers.org/xss.js"></SCRIPT>'))

def method():
    eq(,bleach.clean('<SCRIPT>document.write("<SCRI");</SCRIPT>PT SRC="http://ha.ckers.org/xss.js"></SCRIPT>'))

def method():
    eq(,bleach.clean('<A HREF="http://66.102.7.147/">XSS</A>'))

def method():
    eq(,bleach.clean('<A HREF="http://%77%77%77%2E%67%6F%6F%67%6C%65%2E%63%6F%6D">XSS</A>'))

def method():
    eq(,bleach.clean('<A HREF="http://1113982867/">XSS</A>'))

def method():
    eq(,bleach.clean('<A HREF="http://0x42.0x0000066.0x7.0x93/">XSS</A>'))

def method():
    eq(,bleach.clean('<A HREF="http://0102.0146.0007.00000223/">XSS</A>'))

def method():
    eq(,bleach.clean('<A HREF="h'))

def method():
    eq(,bleach.clean('tt	p://6	6.000146.0x7.147/">XSS</A>'))

def method():
    eq(,bleach.clean('<A HREF="//www.google.com/">XSS</A>'))

def method():
    eq(,bleach.clean('<A HREF="//google">XSS</A>'))

def method():
    eq(,bleach.clean('<A HREF="http://ha.ckers.org@google">XSS</A>'))

def method():
    eq(,bleach.clean('<A HREF="http://google:ha.ckers.org">XSS</A>'))

def method():
    eq(,bleach.clean('<A HREF="http://google.com/">XSS</A>'))

def method():
    eq(,bleach.clean('<A HREF="http://www.google.com./">XSS</A>'))

def method():
    eq(,bleach.clean('<A HREF="javascript:document.location='http://www.google.com/'">XSS</A>'))

def method():
    eq(,bleach.clean('<A HREF="http://www.gohttp://www.google.com/ogle.com/">XSS</A>'))

def method():
    eq(,bleach.clean('&#60;'))

def method():
    eq(,bleach.clean('%3C'))

def method():
    eq(,bleach.clean('&lt'))

def method():
    eq(,bleach.clean('&lt;'))

def method():
    eq(,bleach.clean('&LT'))

def method():
    eq(,bleach.clean('&LT;'))

def method():
    eq(,bleach.clean('&#60'))

def method():
    eq(,bleach.clean('&#060'))

def method():
    eq(,bleach.clean('&#0060'))

def method():
    eq(,bleach.clean('&#00060'))

def method():
    eq(,bleach.clean('&#000060'))

def method():
    eq(,bleach.clean('&#0000060'))

def method():
    eq(,bleach.clean('&#60;'))

def method():
    eq(,bleach.clean('&#060;'))

def method():
    eq(,bleach.clean('&#0060;'))

def method():
    eq(,bleach.clean('&#00060;'))

def method():
    eq(,bleach.clean('&#000060;'))

def method():
    eq(,bleach.clean('&#0000060;'))

def method():
    eq(,bleach.clean('&#x3c'))

def method():
    eq(,bleach.clean('&#x03c'))

def method():
    eq(,bleach.clean('&#x003c'))

def method():
    eq(,bleach.clean('&#x0003c'))

def method():
    eq(,bleach.clean('&#x00003c'))

def method():
    eq(,bleach.clean('&#x000003c'))

def method():
    eq(,bleach.clean('&#x3c;'))

def method():
    eq(,bleach.clean('&#x03c;'))

def method():
    eq(,bleach.clean('&#x003c;'))

def method():
    eq(,bleach.clean('&#x0003c;'))

def method():
    eq(,bleach.clean('&#x00003c;'))

def method():
    eq(,bleach.clean('&#x000003c;'))

def method():
    eq(,bleach.clean('&#X3c'))

def method():
    eq(,bleach.clean('&#X03c'))

def method():
    eq(,bleach.clean('&#X003c'))

def method():
    eq(,bleach.clean('&#X0003c'))

def method():
    eq(,bleach.clean('&#X00003c'))

def method():
    eq(,bleach.clean('&#X000003c'))

def method():
    eq(,bleach.clean('&#X3c;'))

def method():
    eq(,bleach.clean('&#X03c;'))

def method():
    eq(,bleach.clean('&#X003c;'))

def method():
    eq(,bleach.clean('&#X0003c;'))

def method():
    eq(,bleach.clean('&#X00003c;'))

def method():
    eq(,bleach.clean('&#X000003c;'))

def method():
    eq(,bleach.clean('&#x3C'))

def method():
    eq(,bleach.clean('&#x03C'))

def method():
    eq(,bleach.clean('&#x003C'))

def method():
    eq(,bleach.clean('&#x0003C'))

def method():
    eq(,bleach.clean('&#x00003C'))

def method():
    eq(,bleach.clean('&#x000003C'))

def method():
    eq(,bleach.clean('&#x3C;'))

def method():
    eq(,bleach.clean('&#x03C;'))

def method():
    eq(,bleach.clean('&#x003C;'))

def method():
    eq(,bleach.clean('&#x0003C;'))

def method():
    eq(,bleach.clean('&#x00003C;'))

def method():
    eq(,bleach.clean('&#x000003C;'))

def method():
    eq(,bleach.clean('&#X3C'))

def method():
    eq(,bleach.clean('&#X03C'))

def method():
    eq(,bleach.clean('&#X003C'))

def method():
    eq(,bleach.clean('&#X0003C'))

def method():
    eq(,bleach.clean('&#X00003C'))

def method():
    eq(,bleach.clean('&#X000003C'))

def method():
    eq(,bleach.clean('&#X3C;'))

def method():
    eq(,bleach.clean('&#X03C;'))

def method():
    eq(,bleach.clean('&#X003C;'))

def method():
    eq(,bleach.clean('&#X0003C;'))

def method():
    eq(,bleach.clean('&#X00003C;'))

def method():
    eq(,bleach.clean('&#X000003C;'))

def method():
    eq(,bleach.clean('\x3c'))

def method():
    eq(,bleach.clean('\x3C'))

def method():
    eq(,bleach.clean('\u003c'))

def method():
    eq(,bleach.clean('\u003C'))
