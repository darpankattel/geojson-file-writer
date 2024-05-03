from django.shortcuts import render, redirect
from .models import GeoJsonFile, Chunk
from django.http import HttpResponse
from .forms import GeoJsonFileForm, ChunkForm
from .utils import get_feature_collection
from django.contrib import messages as message
import json


def index(request):
    """
    A view to view all files

    """
    files = GeoJsonFile.objects.all()
    return render(request, 'files/index.html', {'files': files})


def detail(request, file_id):
    """
    A view to view the detail of a particular file

    """
    file = GeoJsonFile.objects.get(id=file_id)
    chunks = Chunk.objects.filter(file=file)

    return render(request, 'files/detail.html', {'file': file, 'chunks': chunks})


def markComplete(request, file_id):
    file = GeoJsonFile.objects.get(id=file_id)
    file.completed = True
    file.save()
    return redirect(request.GET.get('next', 'list-files'))


def addChunk(request, file_id):
    if request.method == 'POST':
        form = ChunkForm(request.POST)
        form_id = request.POST.get('id')
        form_id = int(form_id) + 1
        if form.is_valid():
            form.save(file_id=file_id)
            # add initial value to from
            form = ChunkForm(initial={'id': form_id})
            file = GeoJsonFile.objects.get(id=file_id)
            message.success(
                request, 'Chunk added successfully. Add more chunks if needed.'
            )
            return render(request, 'files/addChunk.html', {'form': form, 'file': file})
    else:
        last_chunk = Chunk.objects.filter(
            file=file_id).order_by('id').last()
        if last_chunk is None:
            last_chunk_id = 0
        else:
            last_chunk_id = last_chunk.json["properties"]["id"]
        form = ChunkForm(initial={'id': last_chunk_id + 1})
        file = GeoJsonFile.objects.get(id=file_id)
        return render(request, 'files/addChunk.html', {'form': form, 'file': file})


def deleteChunk(request, file_id, chunk_id):
    chunk = Chunk.objects.get(id=chunk_id)
    chunk.delete()
    return redirect('detail-file', file_id=file_id)


def download(request, file_id):
    file = GeoJsonFile.objects.get(id=file_id)
    chunks = Chunk.objects.filter(file=file).order_by('created_at')
    geo_data = get_feature_collection(chunks)
    output_path = file.get_filepath()
    with open(output_path + '.geojson', 'w') as f:
        f.write(json.dumps(geo_data))
        print(f'{output_path} created')
        file.output = str(
            output_path + '.geojson').split('media\\')[1].replace('\\', '/')
        # file.output = str(output_path + '.geojson')[loc:]
        file.save()
    response = HttpResponse(file.output, content_type='application/json')
    response['Content-Disposition'] = f'attachment; filename="{file.title}.geojson"'
    return response


def create(request):
    if request.method == 'POST':
        form = GeoJsonFileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list-files')
    else:
        form = GeoJsonFileForm()

        return render(request, 'files/create.html', {'form': form})
