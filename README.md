
# DataProxy Plugin for Hyde

A hyde plugin for data driven page generation.

## Usage

**site.yaml**

```yaml
...

plugins:
    - hyde.ext.plugins.meta.MetaPlugin
    ...
    # load plugin
    - dataproxy.DataproxyPlugin
    ...

# data proxy configurations
proxies:
    data:
        # specify the data file path. glob style is allowed here.
        # path should be absolute or relative from site path.
        path: "data/bebop/*.yaml"
    sources:
        # specify template source and relateds.
        -
            # template file path. it should be relative from content directory.
            template: "profiles/hackers_template.html.j2"
            # output file name. jinja2 templating format is allowed.
            # you can use data defined in the data file.
            filename: "profiles/{{ [ firstname, familyname ] | join('_') }}.html"
            # prefix string to access the data in the template.
            # in this case, you can access the data through "resource.character".
            dataprefix: character

        # you can specify the multiple sources.
        -
            template: "tables/table_template.html.j2"
            filename: "tables/{{ [ firstname, familyname ] | join('_') }}.html"
            dataprefix: character
...
```

**data files**

```
$ cd (Hyde's site path)
$ ls data/bebop/*.yaml
Ed.yaml Faye.yaml Jet.yaml Spike.yaml Vicious.yaml
$ cat data/bebop/Spile.yaml

------------
firstname: Spike
familyname: Spiegel
desc: Spike Spiegel is a former member of the Red Dragon Crime Syndicate. Spike is a ...
$ cat data/bebop/Jet.yaml

------------
firstname: Jet
familyname: Black
desc: Jet Black is a former ISSP (Inter-Solar System Police) detective and is the ...
```

**templates**

```jinja2
$ ls content/profiles
profile_template.html.j2
$ cat content/profiles/profile_template.html.j2
---
extends: base.j2
default_block: main
title: bebop character
---
{% set character = resource.character %}

<h3>{{ character.firstname }}'s profile</h3>
<dl>
    <dt><b>Name</b></dt>
    <dd>{{ character.firstname }} {{ character.familyname }}</dd>

    <dt><b>Desc.</b></dt>
    <dd>
    {{ character.desc }}
    </dd>
</dl>
```

**gen command results**

```
$ ls deploy/profiles
Spike_Spiegel.html Jet_Black.html Faye_Valentine.html Edward.html Vicious.html
$ cat deploy/profiles/Jet_Black.html
...
<h3>Jet's profile<h3>
<dl>
    <dt><b>Name</b></dt>
    <dd>Jet Black</dd>

    <dt><b>Desc.</b></dt>
    <dd>
    Jet Black is a former ISSP (Inter-Solar System Police) detective and is the ...
    </dd>
</dl>
...
```

## Problems

* `serve` command does not works correctly for the data diven pages.
* `gen` command does not create the data diven pages under incremental mode
    when the data file has been updated.

**Requires enhancements of Hyde's core code for the plugin.**

