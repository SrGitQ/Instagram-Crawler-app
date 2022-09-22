

def avatarImgH(img):
  return f'<img src="{img}" style="width: 170px; margin:auto; height: 170px; border-radius: 50%; object-fit: cover; display: block;">'

def renderUserName(user):
  return f"<h3 style='color: white;'>{user['User']}</h3>"

def profile_info(user):
  img = avatarImgH('/pics/jmbalanzar/jmbalanzar.png')
  name = renderUserName(user)
  posts = gdBullet('Posts', user['Posts'])
  followers = gdBullet('Followers', user['Followers'])
  following = gdBullet('Following', user['Following'])
  bullets = f'<div style="display: flex; justify-content: space-around; align-items: center;">{posts}{followers}{following}</div>'
  description = f"<p style='color: white;'>{user['Description']}</p>"


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
  """+f"<div class='profile_info_container box' ><div class='avatar'>{img}</div><div class='info'>{name}{bullets}{description}</div></div>"

def gdBullet(label, value):
  return f"<div><h4>{value}</h4><span>{label}<span></div>"