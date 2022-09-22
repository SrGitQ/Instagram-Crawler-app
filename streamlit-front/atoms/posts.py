
comment_icon = '<img src="https://www.freeiconspng.com/uploads/comment-png-17.png" style="width: 15px; height: 15px; object-fit: cover; display: block;">'
like_icon = '<img src="https://static1.hkrtcdn.com/hknext/static/media/common/variant/wishlist/heart-icon.svg" style="width: 15px; height: 15px;object-fit: cover; display: block;">'
def postsIcons():
  return f"<div class='icons'><span></span>{comment_icon}{like_icon}</div>"


def postRow(post):
  img = f'<img src="{post["img"]}" style="width: 50px; height: 50px; border-radius: 50%; object-fit: cover; display: block;">'
  val = f'<div style="display: flex; justify-content: space-around; align-items: center;"><div>{post["Likes"]}</div><div>{post["comments"]}</div></div>'
  values = f'<div class="valuesLayout">{img}<div>{val}</div></div>'

  return values

def topPosts(posts):
  #show only 5 posts
  posts = [f'<div class="alt-box" style="margin:5px">{postRow(post)}</div>' for post in posts]
  return f"<ul>{''.join(posts)}</ul>"