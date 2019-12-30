
from django.urls import path
from . import views

urlpatterns = [
    path('test'                                                     , views.Test),
    path('task/<str:run>'                                           , views.Task),
    path('system'                                                   , views.RESTful_System),
    path('system/<int:id>'                                          , views.RESTful_System),
    path('source'                                                   , views.RESTful_Source),
    path('source/<int:id>'                                          , views.RESTful_Source),
    path('original'                                                 , views.RESTful_Original),
    path('original/<int:id>'                                        , views.RESTful_Original),
    path('original/<str:date>/<int:count>'                          , views.RESTful_Original),
    path('correction'                                               , views.RESTful_Correction),
    path('correction/<int:id>'                                      , views.RESTful_Correction),
    path('correction/<str:date>/<int:count>'                        , views.RESTful_Correction),
    path('avg/minute5'                                              , views.RESTful_Avg5Minute),
    path('avg/minute5/<int:id>'                                     , views.RESTful_Avg5Minute),
    path('avg/minute5/<str:date>/<int:count>'                       , views.RESTful_Avg5Minute),
    path('avg/hour'                                                 , views.RESTful_Avg1Hour),
    path('avg/hour/<int:id>'                                        , views.RESTful_Avg1Hour),
    path('avg/hour/<str:date>/<int:count>'                          , views.RESTful_Avg1Hour),
    path('avg/date'                                                 , views.RESTful_Avg1Date),
    path('avg/date/<int:id>'                                        , views.RESTful_Avg1Date),
    path('avg/date/<str:date>/<int:count>'                          , views.RESTful_Avg1Date),
    path('avg/month'                                                , views.RESTful_Avg1Month),
    path('avg/month/<int:id>'                                       , views.RESTful_Avg1Month),
    path('avg/month/<str:date>/<int:count>'                         , views.RESTful_Avg1Month),
]
