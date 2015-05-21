var width = 960;
var height = 620;

var graphGroups = [];

var svg;
var crtStep = 0;
var force;
var vis;

var chartDataGreen = [];
var chartDataBlue = [];
var chartDataRed = [];

function drawChart() {
    var WIDTH = 960,
        HEIGHT = 200,
        MARGINS = {
            top: 20,
            right: 20,
            bottom: 20,
            left: 50
        };

    if(vis) {
        vis.remove();
    }
    vis = d3.select('#vis').append('svg')
        .attr('width', WIDTH)
        .attr('height', HEIGHT);
        
    var xScale = d3.scale.linear().range([MARGINS.left, WIDTH - MARGINS.right]).domain([0, crtStep]),
        yScale = d3.scale.linear().range([HEIGHT - MARGINS.top, MARGINS.bottom]).domain([0, $('#nodes').val()]),
        xAxis = d3.svg.axis()
            .scale(xScale),
        yAxis = d3.svg.axis()
            .scale(yScale)
            .orient("left");
            
    vis.append("svg:g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + (HEIGHT - MARGINS.bottom) + ")")
        .call(xAxis);
    vis.append("svg:g")
        .attr("class", "y axis")
        .attr("transform", "translate(" + (MARGINS.left) + ",0)")
        .call(yAxis);
    
    var lineGen = d3.svg.line()
                    .x(function(d) {
                        return xScale(d.step);
                    })
                    .y(function(d) {
                        return yScale(d.count);
                    })
                    .interpolate("basis");
                    
    vis.append('svg:path')
        .attr('d', lineGen(chartDataGreen))
        .attr('stroke', 'green')
        .attr('stroke-width', 2)
        .attr('fill', 'none');
    vis.append('svg:path')
        .attr('d', lineGen(chartDataBlue))
        .attr('stroke', 'blue')
        .attr('stroke-width', 2)
        .attr('fill', 'none');
    vis.append('svg:path')
        .attr('d', lineGen(chartDataRed))
        .attr('stroke', 'red')
        .attr('stroke-width', 2)
        .attr('fill', 'none');
}

function getDataUrl(step) {
    var seed = $('#seed').val();
    if(!seed) {
        seed = 1;
    }
    
    var nodes = $('#nodes').val();
    if(!nodes) {
        nodes = 10;
    }
    
    if(!step) {
        step = 0;
    }
    
    return '/data/' + seed + '/' + nodes + '/' + step;
}

start();
    
$('#start').click(start);

$('#step').click(function() {
    crtStep += parseInt($('#stepSize').val());
    
    d3.json(getDataUrl(crtStep), function(error, graph) {
        graphGroups = graph.groups;
        svg.selectAll('.node')
            .style('fill', color);
        
        var counts = _.countBy(graphGroups);
        chartDataGreen.push({
            step: crtStep,
            count: counts.y || 0
        });
        
        chartDataRed.push({
            step: crtStep,
            count: counts.r || 0
        });
        
        chartDataBlue.push({
            step: crtStep,
            count: counts.b || 0
        });
            
        drawChart();
    });
});

function start() {
    chartDataGreen = [];
    chartDataBlue = [];
    chartDataRed = [];
    crtStep = 0;
    
    d3.json(getDataUrl(), function(error, graph) {
        graphGroups = graph.groups;
        
        if(svg) {
            svg.remove();
        }
        svg = d3.select('#canvas').append('svg')
            .attr('width', width)
            .attr('height', height);
        
        force = d3.layout.force()
            .charge(-160)
            .friction(0.7)
            .linkDistance(10)
            .size([width, height]);
            
        var link = svg.selectAll('.link')
            .data(graph.links)
            .enter().append('line')
            .attr('class', 'link')
            .style('stroke-width', 1);

        var node = svg.selectAll('.node')
            .data(graph.nodes)
            .enter().append('circle')
            .attr('class', 'node')
            .attr('r', 5)
            .style('fill', color)
            .call(force.drag);

        force.on('tick', function() {
            link.attr('x1', function(d) { return d.source.x; })
              .attr('y1', function(d) { return d.source.y; })
              .attr('x2', function(d) { return d.target.x; })
              .attr('y2', function(d) { return d.target.y; });

            node.attr('cx', function(d) { return d.x; })
              .attr('cy', function(d) { return d.y; });
        });

        force
          .nodes(graph.nodes)
          .links(graph.links)
          .start();
          
      chartDataGreen.push({
          step: 0,
          count: 3
      });
      
      chartDataRed.push({
          step: 0,
          count: 3
      });
      
      chartDataBlue.push({
          step: 0,
          count: 3
      });
      
      drawChart();
    });
}

function color(d) {
    var group = graphGroups[d.id];
    
    if(group === 'r') {
        return '#ff0000';
    }
    else if(group === 'b') {
        return '#0000ff';
    }
    else if(group === 'y') {
        return '#00ff00';
    }
    
    return '#cccccc';
}

