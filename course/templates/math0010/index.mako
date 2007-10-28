# -*- coding: utf-8 -*-

<%inherit file="/base.mako" />

<%def name="head_tags()">
  <title>St Mary's MATH 0010 Fall 2007/8</title>
  </%def>

<h3 align="center"><a href ="http://www.smu.ca/">
St Mary's University</a></h3>
<h2 align="center"> MATH0010 -- Precalculus I</h2>
<h3 align="center">Fall 2007/8</h3>

<b>Instructor:</b>
<a href="/~peter">Peter Dobcs&aacute;nyi</a>
<br/>
Email: <a href="mailto:peter@cs.smu.ca">peter@cs.smu.ca</a>
<br/>
Office:  McNally North 111
<br/>
Office hours: Monday 11am - 12am, Thursday 7pm - 8pm
<br/>
Phone: (902) 494-1080


<h2>Course Contents</h2>

Elementary set theory and the real number system.  Factorization.
Inequalities, absolute values, and interval notation. Techniques of
solving a variety of equations and inequalities in a single variable.
The Cartesian plane and representation of ordered pairs of real numbers.
Elements of analytic geometry. Relations, functions, and graphs, with
emphasis on the polynomial, exponential, logarithmic functions, and
polynomial and rational equations.

<h2>Required Textbook</h2>

<b>Mark Dugopolski: College Algebra and Trigonometry</b>
<br/>
Fourth Edition, 2007, Pearson
<br/>
ISBN 0-321-35692-6

</p>
In the first semester, Chapters P and 1-4 will be covered.

<h2>Schedule</h2>

<b>Lectures:</b> 5:30 pm - 6:45 pm Tuesday and Thursday, McNally East Wing 110

</p>

<b>Recitation:</b> 7:00 pm - 8:15 pm Tuesday, McNally East Wing 110

<p>You are required to attend both the lectures and the recitation. </p>

<p>
<b>
The Midterm Test will be held on Oct 23 Tuesday at 5:30
in McNally East Wing 110.
</b>

It will contain problems based on all material covered up to the lecture
on Oct 18. In terms of the sections of the textbook, that means: full
Chapter P; full Chapter 1 except 1.5; and Sections 2.1, 2.2 and 2.3 from
Chapter 2.

</p>


<h2>Quizzes, Tests, and Examinations</h2>

<p><b>Quizzes are regularly given during recitations.</b>  They usually
contain questions on material covered since the last quiz. However, they
may include earlier material as well.  </p>

<h4> Rules: </h4>

<ol>

    <li> Except in very special and officially documented cases
    (illness, accident, etc.), quizzes, tests, and examinations must be
    written during the scheduled periods.  Do not make arrangements
    which could potentially conflict.  </li>
    
    <li> No aids will be permitted during quizzes, tests, and
    examinations.  This includes textbooks, notes, calculators and
    electronic devices such as iPods, cell phones, etc.  </li>

    <li> Copying work from another student is prohibited and offenders
    will be subject to academic discipline. All students should be
    familiar with the section of the
    <a href="http://www.smu.ca/registrar/calendar.html">2007-2008 Saint
    Mary's Academic Calendar</a> entitled <i>Academic Integrity and
    Student Responsibility </i> (pp.  22-30) </li>

</ol>

<h2>Evaluation</h2>

<ul>
    <li> <b>20%</b> Quizzes
    <li> <b>30%</b> Midterm test
    <li> <b>50%</b> Final exam
</ul>


<h2>Homework</h2>

<p> After each section of the textbook there is a collection of exercises. Find
the corresponding exercise pages after each lecture and solve at least three
odd numbered problems from every exercise group up to the word problems.  An
exercise group is the collection of problems under the same instruction.</p>

<p> Additional exercises and selected word problems will be announced in
the class. </p>

<p> Homework assignments won't be submitted and graded. You are expected
to check your work from the textbook.  </p>

<h3>Login</h3>

${h.form(h.url_for('math0010', action='login'), method='post')}
Student ID: ${h.text_field('id', value='A')} 
            ${h.submit('login')}
${h.end_form() }
