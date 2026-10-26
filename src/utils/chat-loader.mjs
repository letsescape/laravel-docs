export function createChatLoader({sdkUrl, endpoint, browserManifestUrl = '', loadSDK = () => import(/* webpackIgnore: true */ sdkUrl)}) {
  let instance;
  let loading;
  let currentPage;
  let appliedPage;
  let hidden = false;
  let destroyed = false;

  function applyPage() {
    if (!instance || destroyed) return;
    if (!currentPage) {
      if (!hidden) {
        instance.setVisible(false);
        instance.resetContext();
      }
      hidden = true;
    } else if (currentPage !== appliedPage || hidden) {
      instance.updatePage(currentPage);
      instance.setVisible(true);
      appliedPage = currentPage;
      hidden = false;
    }
  }

  return {
    async update(page) {
      if (destroyed || !sdkUrl || !endpoint) return;
      currentPage = page;
      if (instance) return applyPage();
      if (!currentPage) return;
      if (!loading) {
        loading = loadSDK().then(({initChat}) => {
          if (destroyed || !currentPage) return;
          instance = initChat({
            endpoint,
            page: currentPage,
            ...(browserManifestUrl ? {browserAI: {manifestURL: browserManifestUrl}} : {}),
          });
          appliedPage = currentPage;
        }).finally(() => { loading = undefined; });
      }
      await loading;
      applyPage();
    },
    destroy() {
      if (destroyed) return;
      destroyed = true;
      instance?.destroy();
    },
  };
}
