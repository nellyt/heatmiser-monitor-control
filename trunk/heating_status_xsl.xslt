<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:t="http://www.example.org/history">
	<xsl:template match="/">
		<!-- TODO: Auto-generated template -->
		<html>
		<body>
        <a NAME="Top"></a>
        <br/><a HREF="#Bottom">Bottom</a>
        <table border="1" width="100%">
        <tr>
        <th>Location</th>
        <th>Air</th>
        <th>Remote</th>
        <th>Floor</th>
        <th>Set</th>
        <th>Demand</th>
        </tr>
		<xsl:for-each select="t:poll/t:controller">
			<tr>
                <xsl:call-template name="alternated-row" />
				<td title="location">
					<xsl:value-of select="./t:locationlong" /><sub><xsl:value-of select="./t:ident" /></sub>
				</td>
				<td title="air">
					<xsl:choose>
                        <xsl:when test="./t:sensormode = 0">
							<!-- Air Only -->
							<xsl:value-of select="./t:airtemp" /><sup>o</sup>
						</xsl:when>
                        <xsl:when test="./t:sensormode = 1">
							<!-- Remote Air Only -->
							-
						</xsl:when>
                        <xsl:when test="./t:sensormode = 2">
							<!-- Floor Only -->
							-
						</xsl:when>
                        <xsl:when test="./t:sensormode = 3">
							<!-- Air and floor -->
							<xsl:value-of select="./t:airtemp" /><sup>o</sup>
						</xsl:when>
                        <xsl:when test="./t:sensormode = 4">
							<!-- Remote and floor -->
							-
						</xsl:when>
                        <xsl:otherwise>UNKNWON</xsl:otherwise>
                    </xsl:choose>					
				</td>
				<td title="remote">
					<xsl:choose>
                        <xsl:when test="./t:sensormode = 0">
							<!-- Air Only -->
							-
						</xsl:when>
                        <xsl:when test="./t:sensormode = 1">
							<!-- Remote Air Only -->
							<xsl:value-of select="./t:remtemp" /><sup>o</sup>
						</xsl:when>
                        <xsl:when test="./t:sensormode = 2">
							<!-- Floor Only -->
							-
						</xsl:when>
                        <xsl:when test="./t:sensormode = 3">
							<!-- Air and floor -->
							-
						</xsl:when>
                        <xsl:when test="./t:sensormode = 4">
							<!-- Remote and floor -->
							<xsl:value-of select="./t:remtemp" /><sup>o</sup>
						</xsl:when>
                        <xsl:otherwise>UNKNWON</xsl:otherwise>
                    </xsl:choose>
				</td>
                <td title="floor">
					<xsl:choose>
                        <xsl:when test="./t:sensormode = 0">
							<!-- Air Only -->
							-
						</xsl:when>
                        <xsl:when test="./t:sensormode = 1">
							<!-- Remote Air Only -->
							-
						</xsl:when>
                        <xsl:when test="./t:sensormode = 2">
							<!-- Floor Only -->
							<xsl:value-of select="./t:floortemp" /><sup>o</sup>
						</xsl:when>
                        <xsl:when test="./t:sensormode = 3">
							<!-- Air and floor -->
							<xsl:value-of select="./t:floortemp" /><sup>o</sup>
						</xsl:when>
                        <xsl:when test="./t:sensormode = 4">
							<!-- Remote and floor -->
							<xsl:value-of select="./t:floortemp" /><sup>o</sup>
						</xsl:when>
                        <xsl:otherwise>UNKNWON</xsl:otherwise>
                    </xsl:choose>
				</td>
                <td title="roomset">
                    <xsl:choose>
                        <xsl:when test="./t:onoff = 0">OFF <small>(<xsl:value-of select="./t:roomset" /><sup>o</sup>)</small></xsl:when>
                        <xsl:when test="./t:onoff = 1">
                            <xsl:choose>
                                <xsl:when test="./t:runmode = 0"><xsl:value-of select="./t:roomset" /><sup>o</sup></xsl:when>
                                <xsl:when test="./t:runmode = 1">FROST <small>(<xsl:value-of select="./t:frosttemp" /><sup>o</sup>)</small></xsl:when>
                                <xsl:otherwise>UNKNWON</xsl:otherwise>
                            </xsl:choose>
                        </xsl:when>
                        <xsl:otherwise>UNKNWON</xsl:otherwise>
                    </xsl:choose>
				</td>
                <td title="thisdemand">
                    <xsl:choose>
                        <xsl:when test="./t:thisdemand = 0">-</xsl:when>
                        <xsl:when test="./t:thisdemand = 1"><img src="flame.png"></img></xsl:when>
                        <xsl:otherwise>UNKNWON</xsl:otherwise>
                    </xsl:choose>                    
				</td>
			</tr>
						
        </xsl:for-each>
        <tr>
        <th>Ident</th>
        <th>Air</th>
        <th>Remote</th>
        <th>Floor</th>
        <th>Set</th>
        <th>Demand</th>
        </tr>
		
		</table>
		
		<br/>Based on Poll Made at <xsl:value-of select="t:poll/t:polltime/t:readable" />

        <br/><a HREF="#Top">Top</a>
        <a NAME="Bottom"></a>
		</body>
		</html>
	</xsl:template>
    
    <xsl:template name="alternated-row">
	<!--** Template alternated-row, for alternated rows style in tables -->
	   <xsl:choose>
			<xsl:when test="./t:thisdemand = 0">
				<xsl:attribute name="class">
					<xsl:if test="position() mod 2 = 1">a</xsl:if>
					<xsl:if test="position() mod 2 = 0">b</xsl:if>
				</xsl:attribute>
			</xsl:when>
			<xsl:when test="./t:thisdemand = 1">
				<xsl:attribute name="class">
					<xsl:if test="position() mod 2 = 1">ad</xsl:if>
					<xsl:if test="position() mod 2 = 0">bd</xsl:if>
				</xsl:attribute>
			</xsl:when>
			<xsl:otherwise>
				<xsl:attribute name="class">
					<xsl:if test="position() mod 2 = 1">a</xsl:if>
					<xsl:if test="position() mod 2 = 0">b</xsl:if>
				</xsl:attribute>
			</xsl:otherwise>
		</xsl:choose> 
	</xsl:template>
    
</xsl:stylesheet>
