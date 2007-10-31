# -*- coding: utf-8 -*-

<%inherit file="/base.mako" />

<%def name="head_tags()">
    <title>
    Welcome 
    ${c.student_info.given_names}
    ${c.student_info.surname}
    </title>
    <style>
      blockquote pre{
        font-size: x-large;
      }
    </style>
</%def>

<div style="float: right;">
<a href="${h.url_for('math0010', action='logout')}">logout</a>
&nbsp;
<a href="${h.url_for('math0010')}">back to main page</a>
</div>

<blockquote>
<pre>
${c.message}
</pre>
</blockquote>

<br/>

<div style="float: left; margin-right: 20%;">
  <h3> Student Details </h3>
  <table>
  <tr>
    <th scope="row" class="specalt">ID</th>
    <td class="alt">${c.student_info.id}</td>
  </tr>
  <tr>
    <th scope="row" class="spec">NAME</th>
    <td >${c.student_info.surname}, ${c.student_info.given_names} </td>
  </tr>
  </table> 
</div>

<div style="float: left; margin-right: 20%;"> 
<h3>MARKS</h3> 
<table>
<tr>
  <th scope="col">Test</th>
  <th scope="col">Score</th>
</tr>
<%
class_th = ['spec', 'specalt']
class_td = ['', 'alt']
marks = c.student_marks
%>
% for x in range(len(marks)):
<tr>
  <th scope="row" class="${class_th[x % len(class_th)]}">${marks[x][0]}</th>
  <% y = marks[x]  %>
  % if type(y[1]) == float:
      <td class="${class_td[x % len(class_td)]}">${'%6.2f%%'%y[1]}</td>
  % else:
      <td class="${class_td[x % len(class_td)]}">${'%6s'%y[1]}</td>
  % endif
</tr>
% endfor
</table>
</div>

<div style="float: left; margin-right: 20%;">
  <h3>Downlaods</h3>
  % for x in c.files:
    <div>
      <a href="${h.url_for('/downloads/%s'%x)}">${x}</a> 
    </div>
  % endfor
</div>

<br style="clear: both;"/>
