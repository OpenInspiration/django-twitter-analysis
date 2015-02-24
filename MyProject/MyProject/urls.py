from django.conf.urls import patterns, include, url

from django.contrib import admin

# from MyProject.views import connection_estab

from MyProject.twitanalysis import Output, user_opinion_similarity, topic_opinion_similarity, location_context, forchart

admin.autodiscover()

urlpatterns = patterns('', 
#	url(r'^twt$', connection_estab),
	url(r'^input$', Output),
	url(r'^uos$', user_opinion_similarity),
	url(r'^tos$', topic_opinion_similarity),
	url(r'^location$', location_context),
	url(r'^chart$', forchart)
    # Examples:
    # url(r'^$', 'MyProject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
)
