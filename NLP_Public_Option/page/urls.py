from django.urls import path

import page.views

urlpatterns = [
    path('index/',page.views.index),

    path('home/',page.views.home),

    path('homePageData',page.views.getHomePageData),

    path('hotWord',page.views.hotWord),

    path('articleData',page.views.articleData),

    path('articleDataAnalysis',page.views.articleDataAnalysis),

    path('ipDataAnalysis',page.views.ipDataAnalysis),

    path('commentDataAnalysis',page.views.commentDataAnalysis),

    path('sentimentAnalysis',page.views.sentimentAnalysis),

    path('articleCloud',page.views.articleCloud),

    path('commentCloud',page.views.commentCloud),

    path('commentUserCloud',page.views.commentUserCloud)

]