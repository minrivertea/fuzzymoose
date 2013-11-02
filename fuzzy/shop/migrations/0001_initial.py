# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ShopSettings'
        db.create_table(u'shop_shopsettings', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('postage_price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=2, blank=True)),
            ('postage_discount_threshold', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=2, blank=True)),
            ('homepage_browser_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('google_analytics_script', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'shop', ['ShopSettings'])

        # Adding model 'Category'
        db.create_table(u'shop_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=100)),
            ('description', self.gf('ckeditor.fields.RichTextField')(null=True, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shop.Category'], null=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_navigation_item', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('list_order', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('meta_description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('meta_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('meta_keywords', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'shop', ['Category'])

        # Adding model 'Product'
        db.create_table(u'shop_product', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('long_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=100)),
            ('short_description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('long_description', self.gf('ckeditor.fields.RichTextField')(null=True, blank=True)),
            ('content', self.gf('ckeditor.fields.RichTextField')(null=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shop.Category'])),
            ('meta_description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('meta_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('meta_keywords', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'shop', ['Product'])

        # Adding model 'Review'
        db.create_table(u'shop_review', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('shopper', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shop.Shopper'])),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shop.Product'])),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 11, 1, 0, 0))),
            ('original_text', self.gf('django.db.models.fields.TextField')()),
            ('edited_text', self.gf('django.db.models.fields.TextField')()),
            ('is_published', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'shop', ['Review'])

        # Adding model 'Photo'
        db.create_table(u'shop_photo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('related_product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shop.Product'], null=True, blank=True)),
            ('is_published', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_uploaded', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 11, 1, 0, 0))),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('list_order', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal(u'shop', ['Photo'])

        # Adding model 'Currency'
        db.create_table(u'shop_currency', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('symbol', self.gf('django.db.models.fields.CharField')(max_length=3)),
        ))
        db.send_create_signal(u'shop', ['Currency'])

        # Adding model 'Price'
        db.create_table(u'shop_price', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shop.Product'])),
            ('price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=2, blank=True)),
            ('currency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shop.Currency'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'shop', ['Price'])

        # Adding model 'Discount'
        db.create_table(u'shop_discount', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('value', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('reminder', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'shop', ['Discount'])

        # Adding model 'Shopper'
        db.create_table(u'shop_shopper', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'shop', ['Shopper'])

        # Adding model 'Address'
        db.create_table(u'shop_address', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('shopper', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shop.Shopper'])),
            ('line_1', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('line_2', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('line_3', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('town_city', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('county', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('postcode', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'shop', ['Address'])

        # Adding model 'Page'
        db.create_table(u'shop_page', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=100)),
            ('summary', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('content', self.gf('ckeditor.fields.RichTextField')(null=True, blank=True)),
            ('is_published', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shop.Page'], null=True, blank=True)),
            ('is_top_navigation', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('list_order', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('meta_description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('meta_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('meta_keywords', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'shop', ['Page'])

        # Adding model 'Basket'
        db.create_table(u'shop_basket', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 11, 1, 0, 0))),
        ))
        db.send_create_signal(u'shop', ['Basket'])

        # Adding model 'BasketItem'
        db.create_table(u'shop_basketitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('basket', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shop.Basket'])),
            ('price', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shop.Price'])),
            ('quantity', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'shop', ['BasketItem'])

        # Adding model 'Order'
        db.create_table(u'shop_order', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('shopper', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shop.Shopper'])),
            ('address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shop.Address'], null=True, blank=True)),
            ('discount', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shop.Discount'], null=True, blank=True)),
            ('order_id', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 11, 1, 0, 0))),
            ('date_confirmed', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('date_paid', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'shop', ['Order'])

        # Adding M2M table for field items on 'Order'
        m2m_table_name = db.shorten_name(u'shop_order_items')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('order', models.ForeignKey(orm[u'shop.order'], null=False)),
            ('basketitem', models.ForeignKey(orm[u'shop.basketitem'], null=False))
        ))
        db.create_unique(m2m_table_name, ['order_id', 'basketitem_id'])


    def backwards(self, orm):
        # Deleting model 'ShopSettings'
        db.delete_table(u'shop_shopsettings')

        # Deleting model 'Category'
        db.delete_table(u'shop_category')

        # Deleting model 'Product'
        db.delete_table(u'shop_product')

        # Deleting model 'Review'
        db.delete_table(u'shop_review')

        # Deleting model 'Photo'
        db.delete_table(u'shop_photo')

        # Deleting model 'Currency'
        db.delete_table(u'shop_currency')

        # Deleting model 'Price'
        db.delete_table(u'shop_price')

        # Deleting model 'Discount'
        db.delete_table(u'shop_discount')

        # Deleting model 'Shopper'
        db.delete_table(u'shop_shopper')

        # Deleting model 'Address'
        db.delete_table(u'shop_address')

        # Deleting model 'Page'
        db.delete_table(u'shop_page')

        # Deleting model 'Basket'
        db.delete_table(u'shop_basket')

        # Deleting model 'BasketItem'
        db.delete_table(u'shop_basketitem')

        # Deleting model 'Order'
        db.delete_table(u'shop_order')

        # Removing M2M table for field items on 'Order'
        db.delete_table(db.shorten_name(u'shop_order_items'))


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'shop.address': {
            'Meta': {'object_name': 'Address'},
            'country': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'county': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line_1': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'line_2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'line_3': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'shopper': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shop.Shopper']"}),
            'town_city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'shop.basket': {
            'Meta': {'object_name': 'Basket'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 1, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'shop.basketitem': {
            'Meta': {'object_name': 'BasketItem'},
            'basket': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shop.Basket']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shop.Price']"}),
            'quantity': ('django.db.models.fields.IntegerField', [], {})
        },
        u'shop.category': {
            'Meta': {'object_name': 'Category'},
            'description': ('ckeditor.fields.RichTextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_navigation_item': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'list_order': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'meta_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'meta_keywords': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'meta_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shop.Category']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'})
        },
        u'shop.currency': {
            'Meta': {'object_name': 'Currency'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        },
        u'shop.discount': {
            'Meta': {'object_name': 'Discount'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reminder': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'})
        },
        u'shop.order': {
            'Meta': {'object_name': 'Order'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shop.Address']", 'null': 'True', 'blank': 'True'}),
            'date_confirmed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 1, 0, 0)'}),
            'date_paid': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'discount': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shop.Discount']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'items': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['shop.BasketItem']", 'null': 'True', 'blank': 'True'}),
            'order_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'shopper': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shop.Shopper']"})
        },
        u'shop.page': {
            'Meta': {'object_name': 'Page'},
            'content': ('ckeditor.fields.RichTextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_top_navigation': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'list_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'meta_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'meta_keywords': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'meta_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shop.Page']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'}),
            'summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'shop.photo': {
            'Meta': {'ordering': "('list_order',)", 'object_name': 'Photo'},
            'date_uploaded': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 1, 0, 0)'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'list_order': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'related_product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shop.Product']", 'null': 'True', 'blank': 'True'})
        },
        u'shop.price': {
            'Meta': {'object_name': 'Price'},
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shop.Currency']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shop.Product']"})
        },
        u'shop.product': {
            'Meta': {'object_name': 'Product'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shop.Category']"}),
            'content': ('ckeditor.fields.RichTextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'long_description': ('ckeditor.fields.RichTextField', [], {'null': 'True', 'blank': 'True'}),
            'long_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'meta_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'meta_keywords': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'meta_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'short_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'})
        },
        u'shop.review': {
            'Meta': {'object_name': 'Review'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 1, 0, 0)'}),
            'edited_text': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'original_text': ('django.db.models.fields.TextField', [], {}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shop.Product']"}),
            'shopper': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shop.Shopper']"})
        },
        u'shop.shopper': {
            'Meta': {'object_name': 'Shopper'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'shop.shopsettings': {
            'Meta': {'object_name': 'ShopSettings'},
            'google_analytics_script': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'homepage_browser_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'postage_discount_threshold': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'postage_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'})
        }
    }

    complete_apps = ['shop']