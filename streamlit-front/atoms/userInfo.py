

def avatarImgH(img):
  return f'<img src={img} style="width: 170px; margin:auto; height: 170px; border-radius: 50%; object-fit: cover; display: block;">'

def renderUserName(user):
  return f"<h3 style='color: white;' ><a href='https://www.instagram.com/{user['username']}' style='color: white;'>{user['username']}</a></h3>"

def profile_info(user):
  img = avatarImgH(user['img'])
  name = renderUserName(user)
  posts = gdBullet('Posts', user['no_posts'])
  followers = gdBullet('Followers', user['followers'])
  following = gdBullet('Following', user['following'])
  bullets = f'<div style="display: flex; justify-content: space-around; align-items: center;">{posts}{followers}{following}</div>'
  description = f"<br><p style='color: white;'>{user['bio']}</p>"


  return """
  <style>
    .profile_info_container {
      display: grid;
      grid-template-columns: 1fr 2fr;
      grid-item-margin: 10px;
    }
    .avatar {
      grid-column-start: 1;
      grid-column-end: 1;
    }
    .info {
      grid-column-start: 2;
      grid-column-end: 2;
    }
  </style>
  """+f"<div class='profile_info_container box' style='height:450px' ><br><div class='avatar'>{img}</div><div class='info'>{name}{bullets}{description}</div></div>"

def gdBullet(label, value):
  return f"<div><h4 style='text-align:center'>{value}</h4><p style='text-align:center'>{label}<p></div>"