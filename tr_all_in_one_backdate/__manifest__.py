{
    'name': 'All In One Backdate',
    'version': '19.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Backdate Sale, Purchase, Invoice, Payment and Inventory with remarks',
    'description': """
All In One Backdate — by Technical Rajni
=========================================
Confirm orders and documents with a custom backdate.

Features:
- Sale Order Backdate
- Purchase Order Backdate
- Invoice / Bill Backdate
- Credit Note / Debit Note Backdate
- Payment Backdate
- Inventory / Picking Backdate
- Backdate with Remarks
- Mass Assign Backdate
- Backdate reflects in Stock Moves & Journal Entries
    """,
    'author': 'Technical Rajni',
    'website': 'https://www.technicalrajni.com',
    'license': 'OPL-1',
    'depends': ['sale_management', 'purchase', 'account', 'stock', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_config_settings_views.xml',
        'wizard/backdate_wizard_views.xml',
        'views/sale_order_views.xml',
        'views/purchase_order_views.xml',
        'views/account_move_views.xml',
        'views/stock_picking_views.xml',
    ],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
    'price': 29.00,
    'currency': 'USD',
}
