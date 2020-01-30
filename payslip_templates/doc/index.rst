Documentation
===========================================

Installation
------------
This Module is a standard Odoo Module. Once you purchase it, please follow the following steps to install it:

- A download link will appear on the module description page.

- You need to extract the downloaded file into Odoo 'addons' directory where all other modules are kept.

- You then need to click on ``Updates Apps list`` for the new module to appear on the list of Apps. 

- Then you click on ``Install`` and wait for it to finish

- After that you can go to configure the Logos, colors and your favorite templates as the default templates ...refer to Module ``Description`` for configuration


Configuration
-------------
Please refer to ``Module Description`` for illustrated steps on how to configure


Pre-Installation Requirements
---------------------------

- Download and install ``wkhtmltopdf`` version ``0.12.4 (with patched qt)`` or higher.

Compatibility
------------

- Fully Supports Odoo Version 11.0 Community and Enterprise Editions


Frequently Asked Questions (FAQs)
===========================================


 - The `Header` content is overlapping the `Body` content of the report?

	
	This is usually caused by the `Logo` or the `Company Address` being too large.

	This is not a big problem since in Odoo you can adjust the Paper Sizes to match the size of your logo or Address.

		- If this happens, Enable `Debug/Developer Mode` in Odoo 11.0 in order to access the Extra `Technical Settings` 

		- Go to `Settings -> Technical -> Reports -> Paper Format` and open `European A4`

		- Adjust the `Top Margin` and `Header Spacing` until you get an optima size to match the size of your logo or address
 
