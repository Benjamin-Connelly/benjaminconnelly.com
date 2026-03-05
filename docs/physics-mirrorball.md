# The Physics of a Mirror Ball

A mirror ball is an elegant demonstration of the law of reflection applied across hundreds of tiny mirrors arranged on a sphere. What appears as magical scattered light is actually straightforward geometric optics — each dot on the wall is a real image of the spotlight, reflected by one facet.

---

## 1. Facets as Tiny Plane Mirrors

A standard mirror ball is covered with small, flat, square mirrors — typically 1–2 cm on a side — glued to a spherical shell. Each mirror tile is a plane mirror whose normal vector $\hat{n}$ points radially outward from the sphere's center. Because the sphere has curvature, adjacent facets point in slightly different directions, which is exactly why the reflected beams spread out across the room instead of all converging at one point.

The key insight: **the ball is not a curved mirror**. It's a *piecewise-planar* mirror. Each facet reflects independently according to the law of reflection, and the spherical arrangement simply provides a convenient way to sample many different normal directions.

---

## 2. The Law of Reflection

For a single facet with unit normal $\hat{n}$, incoming light direction $\hat{L}$ (pointing *toward* the facet), the reflected ray direction is:

$$\hat{R} = \hat{L} - 2(\hat{L} \cdot \hat{n})\hat{n}$$

This is the vector form of "angle of incidence equals angle of reflection." The reflected ray $\hat{R}$ lies in the plane defined by $\hat{L}$ and $\hat{n}$, and makes equal angles with $\hat{n}$ on opposite sides.

In our simulation, we compute this for every facet on every frame. The incoming light direction $\hat{L}$ comes from the spotlight (controlled by mouse position), and $\hat{n}$ comes from the facet's position on the sphere (modified by rotation).

---

## 3. Why the Dots Move

As the ball rotates, each facet's normal vector $\hat{n}$ changes direction in world space. If the ball rotates by angle $\theta$ about the vertical axis, a facet at spherical coordinates $(\phi, \theta_0)$ has its azimuthal angle shifted to $\theta_0 + \theta$. The normal becomes:

$$\hat{n} = (\sin\phi\cos(\theta_0 + \theta),\; \cos\phi,\; \sin\phi\sin(\theta_0 + \theta))$$

Since $\hat{R}$ depends on $\hat{n}$, the reflected beam sweeps across the room as the ball turns. Each facet traces out its own arc on the walls and ceiling, and with hundreds of facets all at different latitudes and longitudes, the result is a complex, interlocking pattern of moving dots.

---

## 4. The 2× Angular Amplification

One of the most important properties of reflection: **when a mirror rotates by angle $\alpha$, the reflected beam rotates by $2\alpha$**. This is why mirror ball dots move faster than you might expect — a ball spinning at 2 RPM produces dots that sweep at an angular rate equivalent to 4 RPM relative to the ball's rotation.

The proof is straightforward. If the normal rotates from $\hat{n}$ to $\hat{n}'$ (a rotation of $\alpha$), the change in reflection angle is:

$$\Delta\theta_R = 2\alpha$$

This amplification is what gives mirror balls their dynamic, energetic feel. Even a slowly spinning ball produces fast-moving dots, especially at higher latitudes where the facets have more angular velocity relative to the spotlight.

---

## 5. Why Dots Twinkle

Real mirror ball dots shimmer and flicker. Several effects contribute:

**Surface imperfections.** The mirror tiles aren't perfectly flat — they have slight curvature from being pressed onto the sphere, and the adhesive creates minor warping. These imperfections cause each facet's effective normal to fluctuate slightly as the ball rotates, making the reflected dot wobble and change intensity.

**Facet edges.** As the ball rotates, a facet transitions from facing the spotlight to facing away. Near the boundary (when $\hat{L} \cdot \hat{n} \approx 0$), small changes in angle produce large changes in brightness, creating a rapid on/off flash.

**Specular falloff.** The intensity of the reflected dot depends on $(\hat{L} \cdot \hat{n})^k$ — a power-law falloff that concentrates brightness on facets that are nearly perfectly aligned with the light source. Most facets produce dim reflections; a few produce bright flashes.

In the simulation, we model this with a shimmer term: a sinusoidal perturbation to each facet's normal vector, with random phase offsets per facet, producing the characteristic twinkling effect.

---

## 6. Volumetric Beams (the "God Rays")

In a hazy or smoky room, you can see the actual beams of light connecting the ball to the dots on the walls. This is Tyndall scattering (or Mie scattering for larger particles): the light beam illuminates suspended particles in the air, making the beam path visible.

The beam from each facet follows the reflected ray direction $\hat{R}$, originating at the facet's position on the ball's surface. The visibility of the beam depends on:

- **Particle density**: more haze = more visible beams
- **Beam intensity**: brighter reflections produce more visible beams
- **Viewing angle**: beams are brightest when viewed from the side (90° to the beam), due to the angular dependence of Mie scattering

In the simulation, we approximate this with semi-transparent triangular gradients emanating from the ball center, rotating with the ball. It's a visual approximation rather than a physical simulation, but captures the aesthetic effect.

---

## 7. From Physics to Pixels

The simulation maps the 3D reflected ray $\hat{R}$ to 2D screen coordinates using a spherical projection:

$$x_{\text{screen}} = \frac{W}{2} + \frac{\text{atan2}(R_z, R_x)}{\pi} \cdot \frac{W}{2}$$

$$y_{\text{screen}} = \frac{H}{2} - \frac{\arcsin(R_y)}{\pi/2} \cdot \frac{H}{2}$$

This wraps the full sphere of possible reflection directions onto the rectangular screen, with the forward direction ($+z$) centered. It's an equirectangular projection — the same mapping used for panoramic photos and environment maps.

Each dot is rendered as a radial gradient with two components:
- A **bright core** with radius proportional to $(\hat{L} \cdot \hat{n})^{1.7}$, simulating the concentrated specular reflection
- A **soft halo** with larger radius, simulating bloom and atmospheric scattering

The color shifts toward white at high intensity, simulating photographic overexposure — the same reason bright lights look white regardless of their actual color.

---

*The full simulation runs in real-time using Canvas 2D, with no WebGL or external dependencies. All physics calculations happen on the CPU at 60 fps for ~500 facets.*

---

## 8. Rotational Inertia & Motor Physics

Rather than directly setting angular velocity, the simulation models the ball as a physical rotating body driven by a motor. The ball is a hollow spherical shell (mass $m$, radius $r$), whose moment of inertia is:

$$I = \frac{2}{3}mr^2$$

For a standard disco ball ($m = 2\,\text{kg}$, $r = 0.15\,\text{m}$): $I = 0.03$ kg·m².

The motor applies torque as a proportional controller — torque proportional to the error between target and actual angular velocity:

$$\tau_{\text{motor}} = k_p(\omega_{\text{target}} - \omega)$$

Viscous bearing friction opposes rotation:

$$\tau_{\text{friction}} = -b\,\omega$$

Newton's second law for rotation gives angular acceleration:

$$\alpha = \frac{\tau_{\text{motor}} + \tau_{\text{friction}}}{I} = \frac{k_p(\omega_{\text{target}} - \omega) - b\,\omega}{I}$$

Integration uses the semi-implicit Euler method — velocity updates first, then position uses the corrected velocity:

$$\omega_{n+1} = \omega_n + \alpha \cdot \Delta t \qquad \theta_{n+1} = \theta_n + \omega_{n+1} \cdot \Delta t$$

This is more stable than explicit Euler because the position update already incorporates the velocity correction, reducing energy drift. The system behaves as a first-order lag with time constant $\tau_{\text{sys}} = I/(k_p + b) \approx 0.37\,\text{s}$, reaching 98% of target speed in about 1.5 seconds.

---

## 9. Room Geometry & Perspective Projection

The room view projects reflected beams onto a rectangular room using a pinhole camera model. The ball sits at the origin inside a box (10 × 6 × 12 meters); the camera views from $(0, -1.5, -5)\,\text{m}$ — standing height, one meter inside the near wall — with a 105° field of view.

For each reflected ray $\hat{R}$, we find where it first hits a wall using ray-box intersection. Each wall is an axis-aligned plane, so the intersection parameter for each axis is:

$$t = \frac{d_{\text{wall}}}{R_{\text{component}}}$$

where $d_{\text{wall}}$ is the signed distance to the wall along that axis. Taking the minimum positive $t$ across all six walls gives the first hit, and the 3D intersection point is $\mathbf{P} = t\hat{R}$.

The hit point projects onto the screen through a perspective (pinhole) camera:

$$x_{\text{screen}} = \frac{W}{2} + \frac{P_x}{P_z + d_{\text{cam}}} \cdot f \cdot \frac{W}{2}$$

$$y_{\text{screen}} = \frac{H}{2} - \frac{P_y - y_{\text{cam}}}{P_z + d_{\text{cam}}} \cdot f \cdot \frac{W}{2}$$

where $f = 1/\tan(\text{FOV}/2)$ is the focal ratio, $d_{\text{cam}}$ is the camera distance, and $y_{\text{cam}} = -1.5\,\text{m}$ offsets the camera below the ball to simulate a standing observer looking up at a ceiling-mounted ball. Using $W$ (not $H$) for both axes maintains the correct aspect ratio.

---

## 10. Beam Spread & Elliptical Distortion

Each facet (~1.5 cm) produces a beam that diverges with distance due to the non-collimated spotlight source. The spot size on a wall at distance $t$ is:

$$s_{\text{spot}} = s_{\text{facet}} \cdot \left(1 + \frac{t}{d_{\text{light}}}\right)$$

where $d_{\text{light}}$ is the spotlight-to-ball distance. Closer walls get tighter dots; distant walls get larger, softer ones.

When a beam hits a wall at oblique incidence, the circular beam cross-section projects into an ellipse. If $\theta$ is the angle between the beam and the wall normal:

$$\cos\theta = |\hat{R} \cdot \hat{n}_{\text{wall}}|$$

The semi-minor axis equals the beam radius, while the semi-major axis stretches inversely with $\cos\theta$:

$$a = \frac{s}{\cos\theta}, \quad b = s$$

At normal incidence ($\theta = 0$), the dot is circular. At glancing angles ($\theta \to 90°$), dots elongate into streaks — matching the stretched spots you see near wall edges and corners in real rooms. The ellipse orientation on screen is computed by projecting the beam's tangent-plane component through the camera's perspective Jacobian.

---

## 11. Fresnel Reflectance

Real mirrors don't reflect all light equally — reflectance depends on incidence angle. At near-normal incidence, an aged mirror coating reflects about 70% of incoming light. At grazing angles, reflectance climbs toward 100%. This is the Fresnel effect, modeled with Schlick's approximation:

$$R(\theta) = R_0 + (1 - R_0)(1 - \cos\theta)^5$$

where $R_0 \approx 0.7$ is the base reflectance and $\theta$ is the angle of incidence. The fifth-power falloff means the boost only kicks in at very steep angles — most facets reflect at roughly $R_0$, but edge-on facets flash brighter. The exponent is computed without `Math.pow`: $(1 - \cos\theta)^2$ is squared, then multiplied once more, keeping the per-facet cost to five multiplications.

---

## 12. Spotlight Cone & Penumbra

A real pinspot has finite angular extent — it doesn't illuminate the entire ball uniformly. The simulation models a cone with two angles:

- **Inner cone** (30°): full intensity within this angle from the spotlight axis
- **Outer cone** (65°): zero intensity beyond this angle

Between the two, intensity falls off via a smoothstep function — a cubic Hermite interpolation that produces a smooth, physically plausible penumbra:

$$\text{smoothstep}(a, b, x) = t^2(3 - 2t), \quad t = \text{clamp}\!\left(\frac{x - a}{b - a}\right)$$

The spotlight axis is the light direction vector $\hat{L}$. Since the facet's position on the unit sphere is approximately its normal $\hat{n}$, the angle from the spotlight axis is $\cos^{-1}(\hat{n} \cdot (-\hat{L}))$ — conveniently, this is the same $\cos\theta$ already computed for back-face culling. Moving the light visibly shifts which facets are illuminated.

---

## 13. Inverse-Square Falloff

In the room view, dot brightness attenuates with distance from the ball to the wall. Light intensity follows the inverse-square law — energy spreads over the surface of an expanding sphere. Using a reference distance $d_{\text{ref}}$ for normalization:

$$I(t) = \frac{d_{\text{ref}}^2}{d_{\text{ref}}^2 + t^2}$$

At $t = 0$: full brightness. At $t = d_{\text{ref}}$: half brightness. At $t = 2d_{\text{ref}}$: one-fifth. With $d_{\text{ref}} = 5\,\text{m}$, dots on the near wall are vivid while far-wall dots fade into the background — the same depth cue you perceive in a real room.

This attenuation is applied only in room mode (the panoramic view has no concept of wall distance).

---

## 14. Axis Tilt & Motor Precession

A mirror ball rotating on a perfectly vertical axis produces dots that sweep in horizontal bands — the reflection from each latitude row traces an arc at a fixed height. This creates a visible staircase effect as dots jump between discrete rows.

Real mirror ball motors are never perfectly aligned. The simulation applies a static 10° axis tilt, so dots trace diagonal arcs instead of horizontal bands. On top of this, a slow ±2° wobble oscillates at ~0.13 Hz, with different frequencies for the X and Z tilt components so the motion never exactly repeats.

Mechanically, both are applied as two small-angle rotations (around X then Z) to every facet normal before the shimmer perturbation. The rotation matrices are precomputed once per frame — only their application to each normal costs per-facet work (8 multiplications, 4 additions).

The combined effect is critical: the static tilt eliminates horizontal banding, while the wobble adds organic variation so dots drift slightly between cycles — matching the complex, never-repeating pattern of a real dance floor.

---

## 15. Volumetric Scattering (Smoke)

When smoke is introduced to the room, aerosol particles ($\approx 0.1$–$1\,\mu\text{m}$) shift the optical model from purely specular wall reflections to volumetric Mie scattering along each beam's path. The normally invisible reflected rays become luminous shafts cutting through the space — the same Tyndall effect that makes sunbeams visible through forest canopy on a misty morning.

The scattered intensity reaching the observer depends on the viewing angle $\theta$ between the beam direction $\hat{R}$ and the camera-to-beam vector. We use the **Henyey-Greenstein phase function**:

$$P(\theta) = \frac{1 - g^2}{4\pi(1 + g^2 - 2g\cos\theta)^{3/2}}$$

where $g = 0.6$ is the asymmetry parameter for forward-scattering smoke. At $g = 0$, scattering is isotropic; at $g \to 1$, all light scatters forward. The strong forward lobe means beams traveling roughly toward the camera appear brightest — matching real observation. The denominator is computed as $d \cdot \sqrt{d}$ rather than $d^{3/2}$ to avoid `Math.pow`.

Beam intensity also attenuates with distance through the aerosol via the **Beer-Lambert law**:

$$I(z) = I_0\,e^{-\alpha z}$$

where $\alpha = 0.18\,\text{m}^{-1}$ is the extinction coefficient (absorption + out-scattering). This is applied as a multi-stop linear gradient along each beam polygon, approximating the exponential decay with Canvas 2D gradients.

Smoke density is not uniform — convective currents and thermal plumes create turbulent variation. Rather than simulating full Navier-Stokes fluid dynamics, we modulate beam opacity with a lightweight sine-wave interference pattern:

$$f(x, y, t) = 0.6 + 0.4\,\sin(3.1x + 0.7t)\,\cos(2.7y - 0.5t)$$

The irrational frequency ratios ensure the pattern never exactly repeats, producing organic, non-repeating fluctuation at negligible computational cost.

Each beam is rendered as a narrow quad (widening from ball center to wall hit point) with additive blending (`globalCompositeOperation = 'lighter'`) so overlapping beams accumulate brightness physically.

The ambient haze uses a separate **offscreen canvas** at 1/4 resolution. Eighty drifting particles are rendered there as radial gradients, then composited back onto the main canvas with a gaussian blur pass — the 4× downscale plus blur produces soft, amorphous fog clouds instead of distinct circles. The offscreen canvas uses **temporal persistence**: instead of clearing each frame, a semi-transparent black fill ($\alpha = 0.06$) fades previous content. This causes fog density to accumulate over time and dissipate gradually (~280 frames to fully clear), matching the behavior of real aerosol dispersal.

---

## 16. Rendering Pipeline & Technology

The entire simulation is a single HTML file with no build step, no external libraries, and no WebGL — just the **Canvas 2D API** running on the CPU. All physics and rendering happen in one `requestAnimationFrame` loop at 60 fps for ~650 facets.

The rendering pipeline has seven composited layers, drawn in order each frame:

1. **Background** — solid dark fill (`source-over`)
2. **Cursor glow** — radial gradient at mouse position showing spotlight source
3. **Ball glow** — large radial gradient simulating ambient scatter from the ball body
4. **Decorative beams** — 12 triangular gradients rotating with the ball (`lighter` blending)
5. **Reflected dots** — per-facet physics: normal computation, reflection, ray-box intersection, perspective projection, elliptical rendering with radial gradient halos
6. **Atmospheric haze** — full-screen fog layer, warm glow gradient, and drifting particles rendered to a 1/4-resolution offscreen canvas with temporal persistence, then composited with gaussian blur (`screen` blending)
7. **Bloom** — the full scene is captured at 1/8 resolution, thresholded via `multiply` to extract only bright pixels, then composited back in three passes at increasing blur radii (2px, 8px, 20px) with decreasing opacity — producing a tight hot core, a mid-range aureole, and a wide atmospheric scatter halo (`screen` blending)

Key performance decisions:

- **No per-frame allocation.** Reusable `Float64Array` vectors (N, L, R, P) are written in-place — no objects created during rendering, no GC pressure.
- **Precomputed trig.** Rotation matrices for axis tilt and wobble are computed once per frame, then applied to each facet with 8 multiplies and 4 adds.
- **No `Math.pow`.** Fresnel's fifth-power term uses chained multiplication; Henyey-Greenstein's $d^{3/2}$ uses $d \cdot \sqrt{d}$.
- **Additive blending via Canvas compositing.** `globalCompositeOperation = 'lighter'` gives physically correct light accumulation without shaders.
- **Elliptical dots via `ctx.ellipse()`.** Slightly more expensive than `ctx.arc()`, but captures oblique-incidence distortion without extra geometry.
- **Multi-resolution offscreen canvases.** Haze particles at 1/4 res and bloom at 1/8 res keep GPU fill cost low while the bilinear upscale on `drawImage` provides free smoothing. `ctx.filter` blur runs on the GPU in Chrome/Edge/Firefox.
- **Temporal persistence.** The haze offscreen canvas fades with $\alpha = 0.06$ per frame instead of clearing — fog accumulates and dissipates naturally without extra particle bookkeeping.

The result: a physics-accurate mirror ball simulation that runs anywhere a browser does — desktop, tablet, phone — with zero dependencies and under 1100 lines of code.
