# -*- coding: utf-8 -*-
from django.forms.widgets import Textarea
from django.utils.safestring import mark_safe

class CKEditor(Textarea):

	class Media:
		js = ('/static/js/ckeditor/ckeditor.js',)

	def __init__(self, *args, **kwargs):
		super(CKEditor, self).__init__(*args, **kwargs)

	def render(self, name, value, attrs=None):
		rendered = super(CKEditor, self).render(name, value, attrs)
		###
		txt = mark_safe("""
			<script type="text/javascript"><!--
				jQuery(document).ready(
					function () {
						CKEDITOR.replace('%s', {height:"400", width:"687"});
					}
				);
			//--></script>
		""" % name)
		###
		return ' '.join([rendered, txt,])
