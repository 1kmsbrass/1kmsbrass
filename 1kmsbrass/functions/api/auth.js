export async function onRequestGet({ env }) {
  const clientId = env.GITHUB_CLIENT_ID;
  const redirectUri = "https://1kmsbrass.pages.dev/api/callback";
  const scope = "repo,user";

  const authorizeUrl =
    `https://github.com/login/oauth/authorize?client_id=${clientId}` +
    `&redirect_uri=${encodeURIComponent(redirectUri)}` +
    `&scope=${encodeURIComponent(scope)}`;

  return Response.redirect(authorizeUrl, 302);
}
