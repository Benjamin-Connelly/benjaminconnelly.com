# The Physics of a Disco Ball

A disco ball is an elegant demonstration of the law of reflection applied across hundreds of tiny mirrors arranged on a sphere. What appears as magical scattered light is actually straightforward geometric optics — each dot on the wall is a real image of the spotlight, reflected by one facet.

---

## 1. Facets as Tiny Plane Mirrors

A standard disco ball is covered with small, flat, square mirrors — typically 1–2 cm on a side — glued to a spherical shell. Each mirror tile is a plane mirror whose normal vector $\hat{n}$ points radially outward from the sphere's center. Because the sphere has curvature, adjacent facets point in slightly different directions, which is exactly why the reflected beams spread out across the room instead of all converging at one point.

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

One of the most important properties of reflection: **when a mirror rotates by angle $\alpha$, the reflected beam rotates by $2\alpha$**. This is why disco ball dots move faster than you might expect — a ball spinning at 2 RPM produces dots that sweep at an angular rate equivalent to 4 RPM relative to the ball's rotation.

The proof is straightforward. If the normal rotates from $\hat{n}$ to $\hat{n}'$ (a rotation of $\alpha$), the change in reflection angle is:

$$\Delta\theta_R = 2\alpha$$

This amplification is what gives disco balls their dynamic, energetic feel. Even a slowly spinning ball produces fast-moving dots, especially at higher latitudes where the facets have more angular velocity relative to the spotlight.

---

## 5. Why Dots Twinkle

Real disco ball dots shimmer and flicker. Several effects contribute:

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
