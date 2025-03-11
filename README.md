<div align="center">
    <h1>Trajectopy Web</h1>
    <h3>Simple web interface for quick trajectory comparisons</h3>

This is a simple web interface for comparing trajectories. It is based on [Trajectopy](https://github.com/gereon-t/trajectopy) and implements basic functionality for comparing trajectories.


<p align="center">
  <img style="border-radius: 10px;" src=.images/frontend.png>
</p>

</div>


## Running the image

To run Trajectopy Web, you can use the Docker image available on Docker Hub. The image is available at `gtombrink/trajectopy-web`.

```bash	
docker run -p 8000:8000 -e MAPBOX_TOKEN=<optional mapbox token for map plots> gtombrink/trajectopy-web
```

Trajectopy Web will be available at `http://localhost:8000`.
