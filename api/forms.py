from django import forms

from api.models import Blog

class CreateBlogForm(forms.ModelForm):

    class Meta:
        model = Blog
        fields = ['title', 'description', 'image']

class UpdateBlogForm(forms.ModelForm):

    class Meta:
        model = Blog
        fields = ['title', 'description', 'image']
    
    def save(self, commit=True):
        blog = self.instance
        blog.title = self.cleaned_data['title']
        blog.description = self.cleaned_data['description']

        if self.cleaned_data['image']:
            blog.image = self.cleaned_data['image']

        if commit:
            blog.save()
            
        return blog
    
    