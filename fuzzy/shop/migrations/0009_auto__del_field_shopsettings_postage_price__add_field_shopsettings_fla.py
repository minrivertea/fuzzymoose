# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'ShopSettings.postage_price'
        db.delete_column(u'shop_shopsettings', 'postage_price')

        # Adding field 'ShopSettings.flat_fee_postage_price'
        db.add_column(u'shop_shopsettings', 'flat_fee_postage_price',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=2, blank=True),
                      keep_default=False)

        # Adding field 'ShopSettings.standard_postage_price'
        db.add_column(u'shop_shopsettings', 'standard_postage_price',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=2, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'ShopSettings.postage_price'
        db.add_column(u'shop_shopsettings', 'postage_price',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=2, blank=True),
                      keep_default=False)

        # Deleting field 'ShopSettings.flat_fee_postage_price'
        db.delete_column(u'shop_shopsettings', 'flat_fee_postage_price')

        # Deleting field 'ShopSettings.standard_postage_price'
        db.delete_column(u'shop_shopsettings', 'standard_postage_price')


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
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 22, 0, 0)'}),
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
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 22, 0, 0)'}),
            'date_paid': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'discount': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shop.Discount']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'items': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['shop.BasketItem']", 'null': 'True', 'blank': 'True'}),
            'order_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'preferred_delivery_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'shopper': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shop.Shopper']"})
        },
        u'shop.page': {
            'Meta': {'object_name': 'Page'},
            'content': ('ckeditor.fields.RichTextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_footer_link': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
            'date_uploaded': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 22, 0, 0)'}),
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
            'out_of_stock': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shop.Product']"}),
            'special_postage_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'})
        },
        u'shop.product': {
            'Meta': {'object_name': 'Product'},
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['shop.Category']", 'null': 'True', 'blank': 'True'}),
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
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 22, 0, 0)'}),
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
            'extra_css': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'flat_fee_postage_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'footer_background_color': ('paintstore.fields.ColorPickerField', [], {'max_length': '7', 'null': 'True', 'blank': 'True'}),
            'footer_background_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'footer_logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'google_analytics_script': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'homepage_browser_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link_color': ('paintstore.fields.ColorPickerField', [], {'max_length': '7', 'null': 'True', 'blank': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'main_background_color': ('paintstore.fields.ColorPickerField', [], {'max_length': '7', 'null': 'True', 'blank': 'True'}),
            'main_background_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'postage_discount_threshold': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'standard_postage_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'})
        }
    }

    complete_apps = ['shop']