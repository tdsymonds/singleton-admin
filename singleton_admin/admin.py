from django.contrib import admin
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

class SingletonAdmin(admin.ModelAdmin):
	""" 
	Allows only one instance of a model to be created. This
	can be updated or deleted, but this will prevent additional
	instances being created.
	"""

	def set_message(self, request, action, obj):
		""" 
		Sets the messages returned to the user when an action
		is carried out. 
		"""
		message = ''

		if action == 'Save':
			message = '%s was changed successfully.' % obj
		elif action == 'Save & Continue':
			message = '%s was changed successfully. You can continue editing below.' % obj
		elif action == 'Add':
			message = '%s was added successfully.' % obj
		elif action == 'Add & Continue':
			message = '%s was added successfully. You can continue editing below.' % obj
		elif action == 'Delete':
			message = '%s was deleted successfully.' % obj

		self.message_user(request, message)


	def get_object_url(self):
		""" 
		Tries to get the object url and return it, but if 
		no object exists will return the url to add a new model.
		"""
		try:
			obj = self.model.objects.get()
			url = "admin:%s_%s_change" % (obj._meta.app_label, obj._meta.object_name.lower())
			return reverse(url, args=[obj.id])
		except self.model.DoesNotExist:
			url = "admin:%s_%s_add" % (self.model._meta.app_label, self.model._meta.object_name.lower())
			return reverse(url)
		except:
			return reverse('admin:index')


	def has_add_permission(self, request):
		"""
		Block add permission if a model already exists.
		"""
		if self.get_queryset(self).count() == 0:
			return True
		return False
	

	def response_add(self, request, obj, post_url_continue=None):
		""" 
		If add and continue pressed stay on page, else
		navigate back to admin index.
		"""
		if request.POST.has_key('_continue'):
			self.set_message(request, 'Add & Continue', obj)
			return HttpResponseRedirect(self.get_object_url())
		else:
			self.set_message(request, 'Add', obj)
			return HttpResponseRedirect(reverse('admin:index'))


	def response_change(self, request, obj):
		""" 
		If save and continue pressed stay on page,
		else navigate back to admin index.
		"""
		if request.POST.has_key('_continue'):
			self.set_message(request, 'Save & Continue', obj)
			return HttpResponseRedirect(request.path)
		else:
			self.set_message(request, 'Save', obj)
			return HttpResponseRedirect(reverse('admin:index'))


	def response_delete(self, request, obj_display, obj_id):
		""" 
		If item deleted navigate back to admin index.
		"""
		self.set_message(request, 'Delete', obj_display)
		return HttpResponseRedirect(reverse('admin:index'))


	def changelist_view(self, request):
		"""
		To prevent being able to navigate to the list view,
		either will be navigated to the current model or 
		navigated to the form to add a new model. 
		"""
		return HttpResponseRedirect(self.get_object_url())
