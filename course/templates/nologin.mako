# -*- coding: utf-8 -*-

<%inherit file="/base.mako" />

<%def name="head_tags()">
     <title>St Mary's MATH 0010 Fall 2007/8 Error Page</title>
</%def>

<h3 class='error'>You are not logged in</h3>
<h3>Your session may have expired, 
go to <a href="${h.url_for('math0010')}">main_page</a> to login</h3>
