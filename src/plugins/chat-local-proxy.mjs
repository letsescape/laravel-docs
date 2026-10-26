export default function chatLocalProxy(_context, {target}) {
  const url = new URL(target);
  if (url.protocol !== 'http:' || !['localhost', '127.0.0.1', '[::1]'].includes(url.hostname)
    || url.username || url.password || url.pathname !== '/' || url.search || url.hash) {
    throw new Error('LARAVEL_CHAT_LOCAL_DEMO에는 로컬 데모의 HTTP origin을 지정하세요.');
  }
  return {
    name: 'laravel-chat-local-proxy',
    configureWebpack() {
      return {
        devServer: {
          proxy: [{
            context: ['/__chat'],
            target: url.origin,
            changeOrigin: true,
            pathRewrite: {'^/__chat': ''},
            headers: {origin: url.origin},
          }],
        },
      };
    },
  };
}
