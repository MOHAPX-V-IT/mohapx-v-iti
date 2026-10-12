/* The original 64 × 52 MOHAPX-V-IT crown, extruded rather than replaced.
   Three.js 0.180.0 is self-hosted; see vendor/three-LICENSE.txt. */
const stage = document.getElementById('crownStage');
const control = document.getElementById('motionBtn');
const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');

async function mountCrown() {
  const THREE = await import('./vendor/three.module.min.js');
  const renderer = new THREE.WebGLRenderer({alpha:true,antialias:true,powerPreference:'low-power'});
  renderer.setPixelRatio(Math.min(devicePixelRatio || 1,1.75));
  renderer.setClearColor(0x000000,0);
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.2;
  stage.appendChild(renderer.domElement);

  const scene = new THREE.Scene();
  const camera = new THREE.OrthographicCamera(-40,40,40,-40,.1,400);
  camera.position.set(0,0,150);
  camera.lookAt(0,0,0);

  // An authored studio-light environment, generated locally. No network HDRI.
  const environmentCanvas = document.createElement('canvas');
  environmentCanvas.width = 1024;
  environmentCanvas.height = 512;
  const context = environmentCanvas.getContext('2d');
  const environmentTexture = new THREE.CanvasTexture(environmentCanvas);
  environmentTexture.mapping = THREE.EquirectangularReflectionMapping;
  environmentTexture.colorSpace = THREE.SRGBColorSpace;
  const pmrem = new THREE.PMREMGenerator(renderer);
  let environmentTarget;

  const faceMaterial = new THREE.MeshPhysicalMaterial({color:0xe3a14f,metalness:.9,roughness:.22,clearcoat:1,clearcoatRoughness:.1,envMapIntensity:1.5});
  const edgeMaterial = new THREE.MeshPhysicalMaterial({color:0xf1d2a0,metalness:1,roughness:.16,clearcoat:1,envMapIntensity:1.7});
  const bodyShape = new THREE.Shape();
  // Exact logo path: M6 40 V14 l13 10 L32 4 l13 20 13-10 v26 z.
  bodyShape.moveTo(-26,-14);
  bodyShape.lineTo(-26,12);
  bodyShape.lineTo(-13,2);
  bodyShape.lineTo(0,22);
  bodyShape.lineTo(13,2);
  bodyShape.lineTo(26,12);
  bodyShape.lineTo(26,-14);
  bodyShape.closePath();

  const extrusion = {depth:6,bevelEnabled:true,bevelSegments:8,steps:1,bevelSize:1.1,bevelThickness:1.2,curveSegments:24};
  const bodyGeometry = new THREE.ExtrudeGeometry(bodyShape,extrusion);
  bodyGeometry.translate(0,0,-3);
  const crown = new THREE.Group();
  crown.add(new THREE.Mesh(bodyGeometry,[faceMaterial,edgeMaterial]));

  // The detached rounded base is part of the existing SVG identity.
  const base = new THREE.Shape();
  base.moveTo(-23.5,-24);
  base.lineTo(23.5,-24);
  base.quadraticCurveTo(26,-24,26,-21.5);
  base.quadraticCurveTo(26,-19,23.5,-19);
  base.lineTo(-23.5,-19);
  base.quadraticCurveTo(-26,-19,-26,-21.5);
  base.quadraticCurveTo(-26,-24,-23.5,-24);
  base.closePath();
  const baseGeometry = new THREE.ExtrudeGeometry(base,{...extrusion,bevelSize:.65,bevelThickness:.65});
  baseGeometry.translate(0,0,-3);
  crown.add(new THREE.Mesh(baseGeometry,[faceMaterial,edgeMaterial]));
  crown.rotation.set(-.08,.42,-.1);
  scene.add(crown);
  const key = new THREE.DirectionalLight(0xffe4b8,3);
  key.position.set(-30,40,80);
  const rim = new THREE.DirectionalLight(0xffffff,2);
  rim.position.set(40,10,-30);
  const back = new THREE.DirectionalLight(0xffe4b8,3);
  back.position.set(-25,35,-80);
  scene.add(key,rim,back,new THREE.AmbientLight(0xffffff,1));

  let paused = reducedMotion.matches;
  let visible = true;
  let contextLost = false;
  let frame = 0;
  let lastTime = 0;
  let angle = .42;
  const draw = () => { if (!contextLost) renderer.render(scene,camera); };
  const resize = () => {
    const {width,height} = stage.getBoundingClientRect();
    if (!width || !height) return;
    renderer.setSize(width,height,false);
    const aspect = width/height;
    camera.left = -40*aspect;
    camera.right = 40*aspect;
    camera.updateProjectionMatrix();
    draw();
  };
  const setEnvironment = () => {
    const light = document.documentElement.dataset.theme === 'light';
    const fill = context.createLinearGradient(0,0,0,512);
    fill.addColorStop(0,light ? '#eee8df' : '#414149');
    fill.addColorStop(.48,light ? '#898581' : '#09090c');
    fill.addColorStop(1,light ? '#c8bdae' : '#574938');
    context.fillStyle = fill;
    context.fillRect(0,0,1024,512);
    const bands = [[70,42,160,300],[400,48,65,360],[740,75,175,220]];
    bands.forEach(([x,y,w,h],i) => {
      const grad = context.createLinearGradient(x,0,x+w,0);
      grad.addColorStop(0,'rgba(255,249,237,0)');
      grad.addColorStop(.25,'rgba(255,249,237,.92)');
      grad.addColorStop(.8,'rgba(255,249,237,.92)');
      grad.addColorStop(1,'rgba(255,249,237,0)');
      context.fillStyle = grad;
      context.fillRect(x,y,w,h);
    });
    context.fillStyle = '#f7f5ef';
    context.fillRect(180,35,650,24);
    environmentTexture.needsUpdate = true;
    const nextTarget = pmrem.fromEquirectangular(environmentTexture);
    scene.environment = nextTarget.texture;
    environmentTarget?.dispose();
    environmentTarget = nextTarget;
    draw();
  };
  const tick = time => {
    frame = 0;
    if (paused || !visible || document.hidden || contextLost) { lastTime = 0; return; }
    if (!lastTime) lastTime = time;
    const dt = Math.min((time-lastTime)/1000,.06);
    if (time-lastTime >= 1000/30) {
      angle += dt * (Math.PI*2/28);
      crown.rotation.y = angle;
      crown.rotation.x = -.08 + Math.sin(angle*.7)*.035;
      lastTime = time;
      draw();
    }
    frame = requestAnimationFrame(tick);
  };
  const resume = () => {
    if (!frame && !paused && visible && !document.hidden && !contextLost) {
      lastTime = 0;
      frame = requestAnimationFrame(tick);
    }
  };
  const stop = () => { cancelAnimationFrame(frame);frame=0;lastTime=0; };
  const updateControl = () => {
    control.setAttribute('aria-pressed',String(paused));
    control.querySelector('.motion-text').innerHTML = paused
      ? '<span class="ru">Продолжить вращение</span><span class="en">Resume rotation</span>'
      : '<span class="ru">Остановить вращение</span><span class="en">Pause rotation</span>';
  };
  const setPaused = value => {
    paused = value;
    paused ? stop() : resume();
    updateControl();
  };
  control.addEventListener('click',() => setPaused(!paused));
  reducedMotion.addEventListener('change',event => setPaused(event.matches));
  document.addEventListener('visibilitychange',() => document.hidden ? stop() : resume());
  const observer = new IntersectionObserver(entries => {
    visible = entries[0].isIntersecting;
    visible ? resume() : stop();
  },{threshold:.01});
  observer.observe(stage);
  const resizeObserver = new ResizeObserver(resize);
  resizeObserver.observe(stage);
  const themeObserver = new MutationObserver(setEnvironment);
  themeObserver.observe(document.documentElement,{attributes:true,attributeFilter:['data-theme']});
  renderer.domElement.addEventListener('webglcontextlost',event => {
    event.preventDefault();contextLost=true;stop();stage.classList.remove('is-ready');control.hidden=true;
  });
  renderer.domElement.addEventListener('webglcontextrestored',() => {
    contextLost=false;setEnvironment();resize();stage.classList.add('is-ready');control.hidden=false;resume();
  });
  setEnvironment();
  resize();
  stage.classList.add('is-ready');
  control.hidden = false;
  updateControl();
  resume();
  window.addEventListener('pagehide',event => {
    stop();
    if (event.persisted) return;
    observer.disconnect();resizeObserver.disconnect();themeObserver.disconnect();
    bodyGeometry.dispose();baseGeometry.dispose();faceMaterial.dispose();edgeMaterial.dispose();
    environmentTarget?.dispose();environmentTexture.dispose();pmrem.dispose();renderer.dispose();
  });
  window.addEventListener('pageshow',resume);
}

if (stage && control) mountCrown().catch(() => {
  // Readable, branded SVG remains visible if WebGL or modules are unavailable.
  stage.classList.remove('is-ready');
  control.hidden = true;
});
