<?xml version="1.0" encoding="UTF-8"?>
<!-- 
Extracts the text from a commentarii de bello Gallico html file.

Usage: xsltproc extract_cbg.xslt cbg1.html > cbg1.txt

Author: Erik Bäckerud
-->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <xsl:output method="text" encoding="UTF-8"/>

  <!-- Match the document root and apply templates only to the specific paragraphs -->
  <xsl:template match="/">
    <xsl:apply-templates select="//div[@class='text']/p"/>
  </xsl:template>

  <!-- Template for the paragraphs inside div with class 'text' -->
  <xsl:template match="p">
    <xsl:value-of select="."/>
    <xsl:text>&#10;</xsl:text>
  </xsl:template>

</xsl:stylesheet>
