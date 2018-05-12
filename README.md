# lektor-read-full-post

Allows blog listing posts to be shortened with a link to the full post.

## Install

`lektor plugins add lektor-read-full-post`

## How to Use

Add the `split-text` to a blog post. It must be at the start of a line and be the only text on the line.  
Only text above that line appears on the blog listing page.  
All text appears on the post's dedicated page.   

On the blog listing page, the post will end with the `link-text`, to the full post.

These options can be customized per post body type.

## Config

Create `configs/read-full-post.ini`

This is a full example config
```
always-display = false
markdown-link-text = <br><br>[Read Full Post]({URL_PATH})
markdown-split-text = [//]: # (PLUGIN-READ-FULL-POST)
html-link-text = <br><br><a href="{URL_PATH}">Read Full Post</a>
html-split-text = <!-- PLUGIN-READ-FULL-POST -->
```

`split-text` : The text to split the blog post on.  
`link-text` : The code to link to the full post.  
`always-display` : If `True`, always display the `link-text`. If `False`, only display if blog post contains the `split-text`  
`{URL_PATH}`: Will be replaced with the absolute URL to the full post.

Notice how the configs exist for `html` and `markdown`.  
If the post body type is `markdown`, the `markdown` option is chosen. Same applies for `html`.  
This is detected automatically so if you have another type eg `rst` you can add it.  

## Modify Templates

### blog.html

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

### macros/blog.html

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
The original `post.body` becomes the join split. Therefore the `split-text` no longer exists.   