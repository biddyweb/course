# -*- coding: utf-8 -*-

<%inherit file="/base.mako" />

<%def name="head_tags()">
    <title> Polynom </title>
    <style>
        .fll{float:left;}
        br{clear:both;}
        .cs{text-align:right;}
    </style>
    <script type="text/javascript">
    var number_reg = /^-?[0-9]+$/
    var max_deg = 10
    
    function clear_res()
    {
        document.getElementById("Results").innerHTML= ""
    }

    function generate_fields()
    {
      var len = document.getElementById("degree").value
      var fields = ""
      var cols = new Array("","","","","","","","")
      var i
      if(!len.match(number_reg) || len<1 || len>max_deg)
      {
        document.getElementById("errors").innerHTML=\
            "This division requires polynomials with a positive integer degree"\
            + " <= " + max_deg
        clear_res()
        return false
      }
      document.getElementById("errors").innerHTML=""
      for(i=0; i<len; i++)
      {
        var power=len-i
        cols[i%cols.length] += "<span><input class=\"cs\" value=\"0\" size=\"3\" name=\"c"+i+"\"/>x<sup>"+power+"</sup></span> + <br/>"
      }
        cols[len%cols.length] += "<span><input class=\"cs\" value=\"0\" size=\"3\" name=\"c"+len+"\"/>x<sup>0</sup></span> = 0"
        fields = "<div class=\"fll\">"+cols.join("</div><div class=\"fll\">")+"</div>"
      fields += "<br/> <br/><input type=\"submit\" value=\"Find Roots\" />"
      fields += "<input type=\"hidden\" name=\"degree\" value=\""+len+"\" />"
      document.getElementById("fields").innerHTML=fields
    }

    function check_fields(form)
    {
        var deg = form.degree.value
        var i
        var errors = ""
        if(!deg.match(number_reg) || deg<1 || deg>max_deg)
        {
            document.getElementById("errors").innerHTML=\
            "This division requires polynomials with a positive integer degree"\
            + " <= " + max_deg
            return false
        }
        for(i=0;i<=deg;i++)
        {
            var power=deg-i
            var val = eval("form.c"+i+".value")
            if (!val.match(number_reg)){
               errors += "x<sup>"+power+"</sup> &nbsp;";
           }
        }
        if(errors == ""){
            document.getElementById("errors").innerHTML=""
            return true
        }
        document.getElementById("errors").innerHTML=\
            "The co-effecients for the following variables are missing or invalid &nbsp;"+errors+"."
        return false
    }
</script>

</%def>


<h1>Factoring Polynomials</h1>

<div>
    <span>Degree</span>
    <input name="degree" id="degree" maxlength="2" 
    size="3" onchange="generate_fields()" /> 
    <input type="button" value="Enter" onclick="generate_fields()"/>
</div>

<form method="POST" action="${h.url_for()}"
enctype="application/x-www-form-urlencoded" onsubmit="return check_fields(this)">
    <br/>
    <div id="fields" width="800"></div>
</form>
<div id="errors"></div>
<hr/>

<div id="Results">
% if c.error:
<p>${c.error}</p>
% elif c.polynom_q:
<p> Division &amp; roots for:&nbsp;
    <% 
        y = len(c.polynom_q) 
        printed = False
    %>
    % for x in range(0,y-2):
        % if printed:
            % if c.polynom_q[x] > 1:
                + ${c.polynom_q[x]}x<sup>${y-x-1}</sup>
            % elif c.polynom_q[x] < -1:
                - ${-c.polynom_q[x]}x<sup>${y-x-1}</sup>
            % elif c.polynom_q[x] == -1:
                - x<sup>${y-x-1}</sup>
            % elif c.polynom_q[x] == +1:
                + x<sup>${y-x-1}</sup>
            % endif
        % else:
            % if c.polynom_q[x] != 0:
                <% printed = True %>
                % if abs(c.polynom_q[x])>1:
                    ${c.polynom_q[x]}x<sup>${y-x-1}</sup>
                % elif c.polynom_q[x] == -1:
                    -x<sup>${y-x-1}</sup>
                % else:
                    x<sup>${y-x-1}</sup>
                % endif
            % endif
        % endif
    % endfor
    % if printed:
        % if c.polynom_q[-2] > 1:
            + ${c.polynom_q[-2]}x
        % elif c.polynom_q[-2] < -1:
            - ${-c.polynom_q[-2]}x
        % elif c.polynom_q[-2] == -1:
            - x
        % elif c.polynom_q[-2] == +1:
            + x
        % endif
    % else:
        % if c.polynom_q[-2] != 0:
            <% printed = True %>
            % if abs(c.polynom_q[-2])>1:
                ${c.polynom_q[-2]}x
            % elif c.polynom_q[-2] == -1:
                -x
            % else:
                x
            % endif
        % endif
    % endif
    % if c.polynom_q[-1] > 0:
        + ${c.polynom_q[-1]}
    % elif c.polynom_q[-1] < 0:
        - ${-c.polynom_q[-1]}
    % endif
    = 0
</p>
<pre>
${c.polynom_result}
</pre>
% endif
</div>
