# -*- coding: utf-8 -*-

<%inherit file="/base.mako" />

<%def name="head_tags()">
    <title> Synthetic Division </title>
    <style>
        .fll{float:left;}
        br{clear:both;}
    </style>
    <script type="text/javascript">
    function generate_fields()
    {
      var len = document.getElementById("degree").value
      var fields = ""
      var cols = new Array("","","","","","","","")
      var i
      if(!len.match(/^[0-9]+$/) || len<2)
      {
        document.getElementById("errors").innerHTML=\
            "This division requires polynomials of degree>=2."
        return false
      }
      document.getElementById("errors").innerHTML=""
      for(i=0; i<len; i++)
      {
        var power=len-i
        cols[i%cols.length] += "<span><input dir=\"rtl\" size=\"3\" name=\"c"+i+"\"/>x<sup>"+power+"</sup></span> + <br/>"
      }
        cols[len%cols.length] += "<span><input dir=\"rtl\" size=\"3\" name=\"c"+len+"\"/>x<sup>0</sup></span> = 0"
        fields = "<div class=\"fll\">"+cols.join("</div><div class=\"fll\">")+"</div>"
      fields += "<br/> <br/><input type=\"submit\" value=\"Find Roots\" />"
      document.getElementById("fields").innerHTML=fields
    }

    function check_fields(form)
    {
        var deg = form.degree.value
        var i
        var errors = ""
        if(!deg.match(/^[0-9]+$/) || deg<2)
        {
            document.getElementById("errors").innerHTML=\
            "This division requires polynomials of degree>=2."
            return false
        }
        for(i=0;i<=deg;i++)
        {
            var power=deg-i
            var val = eval("form.c"+i+".value")
            if (!val.match(/^[0-9]+$/)){
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


<h1>Synthetic Division of Polynomials</h1>

<form method="POST" action="${h.url_for('math0010',action='synthetic_calc')}"
target="SyntheticFrame" enctype="application/x-www-form-urlencoded"
onsubmit="return check_fields(this)">
    <div>
        <span>Degree</span>
        <input name="degree" id="degree" maxlength="3" 
        onchange="generate_fields()"
        /> 
<input type="button" value="Generate" onclick="generate_fields()"/>
    </div>
    <br/>
    <div id="fields" width="800"></div>
</form>
<div id="errors"></div>
<iframe id="SyntheticFrame" name="SyntheticFrame"
style="width:800px; height:400px; border: 0px; padding-top:30px;" 
scrolling="auto"></iframe>
