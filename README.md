# lektor-read-full-post
Allows blog listing posts to be shortened with a link to the full post.

## Install

`lektor plugins add lektor-read-full-post`

## How to Use

Add the following split text to your blog post `[//]: # (PLUGIN-READ-FULL-POST)`  
Only text above this line appears on the blog listing page.  
All text appears on the post's dedicated page.   

## Setup

### Config

Create `configs/read-full-post.ini`

```
link-text = Read Full Post
always-display = True
```

`link-text` : The URL text to the blog post.  
`always-display` : If `True`, always display the Read Full Post link. If `False`, only display link if blog post has 
split text.  

Note: To add some new lines you can add `<br>` tags in `link-text` eg `link-text = <br><br>Read Full Post`

### Modify Templates

#### blog.html

This is a full sample of a `blog.html` template  
This new line is required `{% set child = plugin_read_full_post(child) %}`  
This processes the blog post.  
It must come before `render_blog_post`.  

```
{% extends "layout.html" %}
{% from "macros/blog.html" import render_blog_post %}
{% from "macros/pagination.html" import render_pagination %}
{% block title %}{{ this.title }}{% endblock %}
{% block body %}
  {% for child in this.pagination.items %}
    {% set child = plugin_read_full_post(child) %}
    {{ render_blog_post(child, from_index=true) }}
  {% endfor %}

  {{ render_pagination(this.pagination) }}
{% endblock %}
```

#### macros/blog.html

Below are two blocks of template code.  
The first block is the required changes.  
The second block is a full sample of `macros/blog.html` for reference.  


```
  {% if from_index %}
      {{ post.body_short }}
  {% else %}
      {{ post.body }}
  {% endif %}
```

```
{% macro render_blog_post(post, from_index=false) %}
  <div class="blog-post">
  {% if from_index %}
    <h2><a href="{{ post|url }}">{{ post.title }}</a></h2>
  {% else %}
    <h2>{{ post.title }}</h2>
  {% endif %}
  <p class="meta">
    written by
    {% if post.twitter_handle %}
      <a href="https://twitter.com/{{ post.twitter_handle
        }}">{{ post.author or post.twitter_handle }}</a>
    {% else %}
      {{ post.author }}
    {% endif %}
    on {{ post.pub_date }}
  </p>
  {% if from_index %}
      {{ post.body_short }}
  {% else %}
      {{ post.body }}
  {% endif %}
  </div>
{% endmacro %}
```

## How it works

The `post.body` is `deepcopy` to `post.body_short`.  
The blog text is `split()` on the split text.  
Index `0` of the `split()` is used on the blog listing page.  
The original `post.body` is used on the dedicated post's page for the full post.   