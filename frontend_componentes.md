# Componentes Frontend para MewAI

## Estructura de Componentes React

### Componentes Base
```tsx
// Button.tsx - Botón personalizado con variantes
interface ButtonProps {
  variant: 'primary' | 'secondary' | 'outline';
  size: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
  onClick?: () => void;
  isLoading?: boolean;
  // ...otros props
}

// Input.tsx - Campo de entrada con validación
interface InputProps {
  label: string;
  value: string;
  onChange: (value: string) => void;
  error?: string;
  placeholder?: string;
  // ...otros props
}

// Card.tsx - Contenedor tipo tarjeta
interface CardProps {
  title?: string;
  children: React.ReactNode;
  footer?: React.ReactNode;
  // ...otros props
}
```

### Componentes de Diseño
```tsx
// Layout.tsx - Estructura principal de la aplicación
interface LayoutProps {
  children: React.ReactNode;
}

// Sidebar.tsx - Barra lateral de navegación
interface SidebarProps {
  items: NavItem[];
  activeItem?: string;
  onSelectItem: (id: string) => void;
}

// Header.tsx - Barra superior con información de usuario
interface HeaderProps {
  user?: User;
  onLogout: () => void;
}
```

### Componentes de Aplicación

#### Dashboard
```tsx
// DashboardStats.tsx - Estadísticas del usuario
interface DashboardStatsProps {
  contentCount: number;
  imageCount: number;
  projectCount: number;
}

// RecentProjects.tsx - Lista de proyectos recientes
interface RecentProjectsProps {
  projects: Project[];
  onSelectProject: (id: string) => void;
}
```

#### Proyectos
```tsx
// ProjectForm.tsx - Formulario para crear/editar proyectos
interface ProjectFormProps {
  initialData?: Project;
  onSubmit: (data: ProjectFormData) => void;
  isLoading?: boolean;
}

// ProjectList.tsx - Lista de proyectos con filtrado
interface ProjectListProps {
  projects: Project[];
  onSelectProject: (id: string) => void;
  onDeleteProject: (id: string) => void;
}

// ProjectDetail.tsx - Vista detallada de un proyecto
interface ProjectDetailProps {
  project: Project;
  onEdit: () => void;
  onDelete: () => void;
}
```

#### Generación de Contenido
```tsx
// ContentGenerator.tsx - Formulario de generación
interface ContentGeneratorProps {
  onSubmit: (settings: GenerationSettings) => void;
  isGenerating: boolean;
  presets?: GenerationPreset[];
}

// GenerationProgress.tsx - Seguimiento de la generación
interface GenerationProgressProps {
  status: GenerationStatus;
  progress: number;
  currentAgent?: string;
  onCancel: () => void;
}

// ContentPreview.tsx - Vista previa de contenido
interface ContentPreviewProps {
  content: Content;
  selectedPlatform: 'blog' | 'instagram' | 'twitter' | 'linkedin';
  onChangePlatform: (platform: string) => void;
  onEdit: (content: Content) => void;
}
```

#### Visualización de Contenido
```tsx
// ContentViewer.tsx - Visualizador de contenido
interface ContentViewerProps {
  content: Content;
  images?: Image[];
  onExport: (format: string) => void;
}

// BlogPreview.tsx - Vista previa de blog
interface BlogPreviewProps {
  title: string;
  content: string;
  images?: Image[];
}

// SocialMediaPreview.tsx - Vista previa para redes sociales
interface SocialMediaPreviewProps {
  platform: 'instagram' | 'twitter' | 'linkedin';
  content: string;
  image?: Image;
}
```

#### Imágenes
```tsx
// ImageGallery.tsx - Galería de imágenes generadas
interface ImageGalleryProps {
  images: Image[];
  onSelectImage: (id: string) => void;
  onDeleteImage: (id: string) => void;
}

// ImageGenerator.tsx - Formulario para generar imágenes
interface ImageGeneratorProps {
  onSubmit: (prompt: string, format: string) => void;
  isGenerating: boolean;
}
```

## Gestión de Estado

### Hooks Personalizados
```tsx
// useUser.tsx - Gestión de autenticación
function useUser() {
  // Estado para el usuario actual, funciones de login/logout
  return {
    user,
    login,
    logout,
    register,
    isLoading,
    error
  };
}

// useProjects.tsx - Gestión de proyectos
function useProjects() {
  // CRUD de proyectos
  return {
    projects,
    createProject,
    updateProject,
    deleteProject,
    isLoading,
    error
  };
}

// useGeneration.tsx - Control del proceso de generación
function useGeneration() {
  // Estado y control de generación
  return {
    startGeneration,
    cancelGeneration,
    generationStatus,
    progress,
    currentAgent,
    isGenerating,
    error
  };
}
```

## Páginas Principales

```tsx
// pages/Dashboard.tsx
export function Dashboard() {
  const { projects } = useProjects();
  const recentProjects = projects.slice(0, 5);
  
  return (
    <Layout>
      <h1>Panel de Control</h1>
      <DashboardStats />
      <RecentProjects projects={recentProjects} />
      <QuickActions />
    </Layout>
  );
}

// pages/NewProject.tsx
export function NewProject() {
  const { createProject } = useProjects();
  
  return (
    <Layout>
      <h1>Nuevo Proyecto</h1>
      <ProjectForm onSubmit={createProject} />
    </Layout>
  );
}

// pages/ProjectDetail.tsx
export function ProjectDetail({ projectId }) {
  const { project, updateProject, deleteProject } = useProject(projectId);
  
  return (
    <Layout>
      <h1>{project.title}</h1>
      <ProjectDetail 
        project={project}
        onEdit={handleEdit}
        onDelete={handleDelete}
      />
      <ContentViewer content={project.contents} />
    </Layout>
  );
}
```

## Integración con API

```tsx
// api/client.ts - Cliente Axios configurado
const apiClient = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json'
  }
});

// api/auth.ts - Servicios de autenticación
export const authService = {
  login: (email, password) => 
    apiClient.post('/auth/login', { email, password }),
  
  register: (userData) => 
    apiClient.post('/auth/register', userData),
  
  me: () => 
    apiClient.get('/auth/me')
};

// api/projects.ts - Servicios de proyectos
export const projectService = {
  getAll: () => 
    apiClient.get('/projects'),
  
  getById: (id) => 
    apiClient.get(`/projects/${id}`),
  
  create: (data) => 
    apiClient.post('/projects', data),
  
  update: (id, data) => 
    apiClient.put(`/projects/${id}`, data),
  
  delete: (id) => 
    apiClient.delete(`/projects/${id}`)
};

// api/generation.ts - Servicios de generación
export const generationService = {
  start: (settings) => 
    apiClient.post('/generation/start', settings),
  
  getStatus: (id) => 
    apiClient.get(`/generation/${id}`),
  
  stop: (id) => 
    apiClient.post(`/generation/${id}/stop`)
};
``` 