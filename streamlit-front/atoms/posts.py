
scope_icon = '<img src="https://cdn3.iconfinder.com/data/icons/basic-ui-elements-2-4-black-fill/512/Basic_UI_Elements_2.4_-_Black_Fill-30-512.png" style="width: 25px; height: 25px; object-fit: cover; display: block;">'
like_icon = '<img src="https://static1.hkrtcdn.com/hknext/static/media/common/variant/wishlist/heart-icon.svg" style="width: 25px; height: 25px;object-fit: cover; display: block;">'
def postsIcons():
  return f"<div class='icons'><span></span>{like_icon}{scope_icon}</div>"


def postRow(post):
  img = f'<a href="{post["url"]}"><img src="{post["display"]}" style="width: 60px; height: 60px; border-radius: 50%; object-fit: cover; display: block;"></a>'
  val = f'<div style=" display: flex; justify-content: space-around; align-items: center;"><div>{post["likes"]}</div><div>{post["scopePercent"]}</div></div>'
  values = f'<div class="valuesLayout">{img}<div style="padding-top:15px">{val}</div></div>'

  return values

def topPosts(posts):
  #show only 5 posts
  posts = [f'<div class="alt-box" style="margin:5px">{postRow(post)}</div>' for post in posts[:5]]
  return f"<ul>{''.join(posts)}</ul>"