{
    "name": "Rest API",
    "version": "0.0.1",
    "category": "API",
    "author": "KhmerDev",
    "website": "https://www.khmerdev.com/",
    "summary": "Restful API",
    "support": "contact@khmerdev.com",
    "description": """
RESTFUL API For Odoo
====================
With use of this module user can enable REST API in any Odoo applications/modules
""",
    "depends": ["web", "base"],
    "data": [
        "data/ir_config_param.xml",
        "views/ir_model.xml",
        "views/res_users.xml",
        "security/ir.model.access.csv",
    ],
    "images": ["static/description/main_screenshot.png"],
    "license": "LGPL-3",
    "installable": True,
    "auto_install": False,
}
