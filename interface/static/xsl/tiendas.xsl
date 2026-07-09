<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet
  version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
>

  <xsl:template match="/">
    <div class="xml-report">
      <h2>Reporte de Tiendas</h2>

      <table>
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Dirección</th>
            <th>Categoría</th>
            <th>Estado</th>
          </tr>
        </thead>

        <tbody>
          <xsl:for-each select="tiendas/tienda">
            <tr>
              <td>
                <xsl:value-of select="nombre" />
              </td>

              <td>
                <xsl:value-of select="direccion" />
              </td>

              <td>
                <xsl:value-of select="categoria" />
              </td>

              <td>
                <xsl:value-of select="estado" />
              </td>
            </tr>
          </xsl:for-each>
        </tbody>
      </table>
    </div>
  </xsl:template>

</xsl:stylesheet>