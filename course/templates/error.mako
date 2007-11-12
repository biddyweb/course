# -*- coding: utf-8 -*-

<%inherit file="/base.mako" />

<%def name="head_tags()">
     <title>St Mary's MATH 0010 Fall 2007/8 Error Page</title>
</%def>

<h3 class='error'>${c.error_msg}</h3>
<br/>
<a href="${h.url_for('math0010')}">main_page</a>
